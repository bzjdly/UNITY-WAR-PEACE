#!/usr/bin/env sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
cd "$repo_root"

if ! command -v git >/dev/null 2>&1; then
  echo "Git is not installed or is not available on PATH." >&2
  exit 1
fi

git lfs install --local

merge_tool=${UNITY_YAML_MERGE:-}

if [ -z "$merge_tool" ]; then
  project_version=""
  if [ -f "ProjectSettings/ProjectVersion.txt" ]; then
    project_version=$(sed -n 's/^m_EditorVersion:[[:space:]]*//p' "ProjectSettings/ProjectVersion.txt" | head -n 1)
  fi

  if [ -n "$project_version" ]; then
    for candidate in \
      "$HOME/Unity/Hub/Editor/$project_version/Editor/Data/Tools/UnityYAMLMerge" \
      "/Applications/Unity/Hub/Editor/$project_version/Unity.app/Contents/Tools/UnityYAMLMerge"
    do
      if [ -x "$candidate" ]; then
        merge_tool=$candidate
        break
      fi
    done
  fi
fi

if [ -z "$merge_tool" ]; then
  for candidate in \
    "$HOME/Unity/Hub/Editor"/*/Editor/Data/Tools/UnityYAMLMerge \
    "/Applications/Unity/Hub/Editor"/*/Unity.app/Contents/Tools/UnityYAMLMerge
  do
    if [ -x "$candidate" ]; then
      merge_tool=$candidate
      break
    fi
  done
fi

if [ -z "$merge_tool" ] || [ ! -x "$merge_tool" ]; then
  echo "UnityYAMLMerge was not found. Git LFS is configured, but Unity SmartMerge is not." >&2
  echo "Set UNITY_YAML_MERGE to the UnityYAMLMerge path and run this script again." >&2
  exit 0
fi

git config merge.unityyamlmerge.name "Unity SmartMerge"
git config merge.unityyamlmerge.driver "\"$merge_tool\" merge -p %O %B %A %A"
git config merge.unityyamlmerge.recursive binary

echo "Git LFS and Unity SmartMerge are configured."
echo "UnityYAMLMerge: $merge_tool"
