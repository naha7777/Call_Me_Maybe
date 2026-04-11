#!/bin/bash
set -e

# ─── Cache dirs ───────────────────────────────────────────
export PIP_CACHE_DIR="/goinfre/$USER/pip-cache"
export UV_CACHE_DIR="/goinfre/$USER/uv-cache"
export HF_HOME="/goinfre/$USER/hf-cache"
export TRANSFORMERS_CACHE="/goinfre/$USER/hf-cache"

mkdir -p "$PIP_CACHE_DIR" "$UV_CACHE_DIR" "$HF_HOME"
echo "✓ Cache dirs configurés dans /goinfre/$USER"

# ─── Install uv ───────────────────────────────────────────
if ! command -v uv &> /dev/null; then
    curl -Ls https://astral.sh/uv/install.sh | UV_INSTALL_DIR="/goinfre/$USER/uv" sh
    export PATH="/goinfre/$USER/uv/bin:$PATH"
    echo "✓ uv installé"
else
    echo "✓ uv déjà présent"
fi

# curl -Ls https://astral.sh/uv/install.sh | UV_INSTALL_DIR="/goinfre/$USER/uv" sh
# export PATH="/goinfre/$USER/uv/bin:$PATH"
# echo "✓ uv installé"

# ─── Venv dans goinfre ────────────────────────────────────
uv venv "/goinfre/$USER/call_me_maybe_venv"
rm -rf .venv
ln -s "/goinfre/$USER/call_me_maybe_venv" .venv
echo "✓ Venv créée et liée"

# ─── Dépendances du projet ────────────────────────────────
uv sync
echo "✓ Dépendances installées"

echo ""
echo "Lancer avec :"
echo "source .venv/bin/activate"

export HF_HOME="/goinfre/$USER/hf-cache"

echo "\nsi transformers manquant 'uv pip install transformers'"

echo "Exporter dernier variable pour Hugging Face"
echo "export HF_HOME="/goinfre/$USER/hf-cache""
