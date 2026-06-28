#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'EOF'
Usage: scripts/reset-disco-home.sh [options]

Reset ~/.disco back to the state expected after a fresh source build, while
preserving user-level configuration files:

  ~/.disco/agent/auth.json
  ~/.disco/agent/settings.json
  ~/.disco/agent/models.json

The ~/.disco/agent/skills directory is preserved unless you explicitly confirm
deleting it when running with --force.

By default this script only prints what it would do. Pass --force to delete
runtime state such as sessions, imported skills, generated environments,
workflow runs, tools, prompts, themes, logs, and other files under ~/.disco.

Options:
  -f, --force                 Perform the reset.
      --backup                Copy the current ~/.disco to a timestamped
                              backup before resetting.
      --disco-dir PATH   Reset PATH instead of ~/.disco. This is
                              intended for testing the script.
  -h, --help                  Show this help.
EOF
}

die() {
	echo "error: $*" >&2
	exit 1
}

expand_tilde() {
	local path="$1"
	case "$path" in
		"~")
			printf '%s\n' "${HOME:?}"
			;;
		~/*)
			printf '%s/%s\n' "${HOME:?}" "${path#~/}"
			;;
		*)
			printf '%s\n' "$path"
			;;
	esac
}

force=0
backup=0
disco_dir="${HOME:-}/.disco"

while [[ $# -gt 0 ]]; do
	case "$1" in
		-f | --force)
			force=1
			;;
		--backup)
			backup=1
			;;
		--disco-dir)
			[[ $# -ge 2 ]] || die "--disco-dir requires a path"
			disco_dir="$2"
			shift
			;;
		--disco-dir=*)
			disco_dir="${1#*=}"
			;;
		-h | --help)
			usage
			exit 0
			;;
		*)
			die "unknown option: $1"
			;;
	esac
	shift
done

[[ -n "${HOME:-}" ]] || die "HOME is not set"
disco_dir="$(expand_tilde "$disco_dir")"
agent_dir="$disco_dir/agent"
skills_dir="$agent_dir/skills"
preserved_names=(auth.json settings.json models.json)

case "$disco_dir" in
	"" | "/" | "$HOME")
		die "refusing to reset unsafe path: $disco_dir"
		;;
esac

if [[ -L "$disco_dir" ]]; then
	die "$disco_dir is a symlink; refusing to reset through a symlink"
fi

if [[ -e "$disco_dir" && ! -d "$disco_dir" ]]; then
	die "$disco_dir exists but is not a directory"
fi

if [[ -L "$agent_dir" ]]; then
	die "$agent_dir is a symlink; refusing to reset through a symlink"
fi

confirm_delete_skills() {
	delete_skills=0
	if [[ ! -e "$skills_dir" && ! -L "$skills_dir" ]]; then
		return
	fi

	echo
	printf 'Delete %s? Type uppercase Y to confirm: ' "$skills_dir"
	local answer
	if ! IFS= read -r answer; then
		echo
		echo "No confirmation received; preserving $skills_dir"
		return
	fi

	case "$answer" in
		Y)
			delete_skills=1
			echo "Confirmed: $skills_dir will be deleted."
			;;
		*)
			echo "Preserving $skills_dir"
			;;
	esac
}

show_plan() {
	echo "Target: $disco_dir"
	echo
	echo "Preserve if present:"

	local preserved_found=0
	local name
	for name in "${preserved_names[@]}"; do
		local path="$agent_dir/$name"
		if [[ -f "$path" || -L "$path" ]]; then
			echo "  - $path"
			preserved_found=1
		fi
	done
	if [[ -e "$skills_dir" || -L "$skills_dir" ]]; then
		echo "  - $skills_dir unless deletion is confirmed during --force"
		preserved_found=1
	fi
	if [[ "$preserved_found" -eq 0 ]]; then
		echo "  - none found"
	fi

	echo
	if [[ ! -e "$disco_dir" ]]; then
		echo "Nothing to remove: $disco_dir does not exist."
		return
	fi

	echo "Remove:"
	local entry_found=0
	while IFS= read -r entry; do
		entry_found=1
		if [[ "$entry" == "$agent_dir" ]]; then
			echo "  - $entry/* except preserved entries listed above"
		else
			echo "  - $entry"
		fi
	done < <(find "$disco_dir" -mindepth 1 -maxdepth 1 -print | sort)

	if [[ "$entry_found" -eq 0 ]]; then
		echo "  - nothing"
	fi
}

show_plan

if [[ "$force" -ne 1 ]]; then
	echo
	echo "Dry run only. Re-run with --force to reset."
	exit 0
fi

if [[ ! -e "$disco_dir" ]]; then
	echo
	echo "Done: nothing to reset."
	exit 0
fi

confirm_delete_skills

if [[ "$backup" -eq 1 ]]; then
	timestamp="$(date +%Y%m%d-%H%M%S)"
	backup_dir="${disco_dir}.backup-${timestamp}"
	if [[ -e "$backup_dir" ]]; then
		backup_dir="${backup_dir}.$$"
	fi
	echo
	echo "Creating backup: $backup_dir"
	cp -a "$disco_dir" "$backup_dir"
fi

tmp_dir="$(mktemp -d "${TMPDIR:-/tmp}/disco-reset.XXXXXX")"
restore_complete=0
cleanup() {
	local status=$?
	if [[ "$status" -ne 0 && "$restore_complete" -ne 1 ]]; then
		echo "Preserved file copies are still available at: $tmp_dir" >&2
	else
		rm -rf -- "$tmp_dir"
	fi
	exit "$status"
}
trap cleanup EXIT

tmp_agent_dir="$tmp_dir/agent"
mkdir -p "$tmp_agent_dir"

preserved_count=0
for name in "${preserved_names[@]}"; do
	src="$agent_dir/$name"
	if [[ -f "$src" || -L "$src" ]]; then
		cp -a "$src" "$tmp_agent_dir/$name"
		preserved_count=$((preserved_count + 1))
	fi
done

preserve_skills=0
if [[ "$delete_skills" -ne 1 && ( -e "$skills_dir" || -L "$skills_dir" ) ]]; then
	cp -a "$skills_dir" "$tmp_agent_dir/skills"
	preserve_skills=1
fi

echo
echo "Removing runtime state under $disco_dir"
rm -rf -- "$disco_dir"

if [[ "$preserved_count" -gt 0 || "$preserve_skills" -eq 1 ]]; then
	echo "Restoring preserved agent data"
	mkdir -p "$agent_dir"
	for name in "${preserved_names[@]}"; do
		src="$tmp_agent_dir/$name"
		if [[ -f "$src" || -L "$src" ]]; then
			cp -a "$src" "$agent_dir/$name"
		fi
	done
	if [[ "$preserve_skills" -eq 1 ]]; then
		cp -a "$tmp_agent_dir/skills" "$skills_dir"
	fi
fi

restore_complete=1
echo "Done."
