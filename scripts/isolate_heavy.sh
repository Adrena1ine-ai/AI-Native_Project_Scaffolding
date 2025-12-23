#!/usr/bin/env bash
set -euo pipefail

PROJ="$(basename "$PWD")"

VENV_HOME="../_venvs"
ART_HOME="../_artifacts/${PROJ}"
DATA_HOME="../_data/${PROJ}"

mkdir -p "$VENV_HOME" "$ART_HOME" "$DATA_HOME"

move_if_exists () {
  local src="$1"
  local dst="$2"
  if [ -e "$src" ]; then
    echo "Move: $src -> $dst"
    rm -rf "$dst"
    mv "$src" "$dst"
  fi
}

# Environments -> ../_venvs (реюз без дубликатов)
move_if_exists "venv"        "${VENV_HOME}/${PROJ}-main"
move_if_exists "venv_gate"   "${VENV_HOME}/${PROJ}-gate"
move_if_exists ".venv"       "${VENV_HOME}/${PROJ}-dotvenv"
move_if_exists "parser_faberlic_links/.venv_parser" "${VENV_HOME}/${PROJ}-parser"

# Logs -> ../_artifacts/<proj>/logs
if [ -d "logs" ]; then
  echo "Move: logs -> ${ART_HOME}/logs"
  mkdir -p "${ART_HOME}"
  rm -rf "${ART_HOME}/logs"
  mv "logs" "${ART_HOME}/logs"
fi

# Parser CSV dumps -> ../_data/<proj>/parser_csv (опционально, но красиво)
if compgen -G "parser_faberlic_links/*.csv" > /dev/null; then
  mkdir -p "${DATA_HOME}/parser_csv"
  echo "Move: parser_faberlic_links/*.csv -> ${DATA_HOME}/parser_csv/"
  mv parser_faberlic_links/*.csv "${DATA_HOME}/parser_csv/" || true
fi

echo
echo "Done."
echo "Venvs:     ${VENV_HOME}/"
echo "Artifacts: ${ART_HOME}/"
echo "Data:      ${DATA_HOME}/"

