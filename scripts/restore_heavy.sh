#!/usr/bin/env bash
set -euo pipefail

PROJ="$(basename "$PWD")"

VENV_HOME="../_venvs"
ART_HOME="../_artifacts/${PROJ}"
DATA_HOME="../_data/${PROJ}"

restore_if_exists () {
  local src="$1"
  local dst="$2"
  if [ -e "$src" ]; then
    echo "Restore: $src -> $dst"
    rm -rf "$dst"
    mkdir -p "$(dirname "$dst")"
    mv "$src" "$dst"
  fi
}

# Restore envs back into repo (обычно НЕ надо; только если ты так хочешь)
restore_if_exists "${VENV_HOME}/${PROJ}-main" "venv"
restore_if_exists "${VENV_HOME}/${PROJ}-gate" "venv_gate"
restore_if_exists "${VENV_HOME}/${PROJ}-dotvenv" ".venv"
restore_if_exists "${VENV_HOME}/${PROJ}-parser" "parser_faberlic_links/.venv_parser"

# Restore logs
if [ -d "${ART_HOME}/logs" ]; then
  echo "Restore: ${ART_HOME}/logs -> ./logs"
  rm -rf "logs"
  mv "${ART_HOME}/logs" "logs"
fi

# Restore CSV dumps
if [ -d "${DATA_HOME}/parser_csv" ]; then
  echo "Restore: ${DATA_HOME}/parser_csv/*.csv -> parser_faberlic_links/"
  mv "${DATA_HOME}/parser_csv/"*.csv "parser_faberlic_links/" 2>/dev/null || true
fi

echo "Done."

