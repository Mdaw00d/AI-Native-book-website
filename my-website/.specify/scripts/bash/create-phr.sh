#!/bin/bash

# Prompt History Record (PHR) Creation Script
# Creates a new PHR from template with proper ID allocation and routing

set -e

# Default values
STAGE="general"
FEATURE="none"
TITLE=""
JSON_OUTPUT=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --title)
      TITLE="$2"
      shift 2
      ;;
    --stage)
      STAGE="$2"
      shift 2
      ;;
    --feature)
      FEATURE="$2"
      shift 2
      ;;
    --json)
      JSON_OUTPUT=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate required arguments
if [ -z "$TITLE" ]; then
  echo "Error: --title is required"
  exit 1
fi

# Valid stages
VALID_STAGES=("constitution" "spec" "plan" "tasks" "red" "green" "refactor" "explainer" "misc" "general")
if [[ ! " ${VALID_STAGES[@]} " =~ " ${STAGE} " ]]; then
  echo "Error: Invalid stage '$STAGE'. Must be one of: ${VALID_STAGES[*]}"
  exit 1
fi

# Create slug from title
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//')

# Determine route based on stage
if [ "$STAGE" = "constitution" ]; then
  ROUTE="history/prompts/constitution"
  EXTENSION="constitution.prompt.md"
elif [ "$STAGE" = "general" ]; then
  ROUTE="history/prompts/general"
  EXTENSION="general.prompt.md"
else
  # Feature stages
  if [ "$FEATURE" = "none" ] || [ -z "$FEATURE" ]; then
    # Try to detect feature from current branch
    BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
    if [ "$BRANCH" != "main" ] && [ "$BRANCH" != "master" ]; then
      FEATURE="$BRANCH"
    else
      echo "Error: Feature stages require --feature argument or feature branch"
      exit 1
    fi
  fi
  ROUTE="history/prompts/$FEATURE"
  EXTENSION="$STAGE.prompt.md"
fi

# Create route directory
mkdir -p "$ROUTE"

# Find next available ID
ID=1
while [ -f "$ROUTE/$ID-"*".md" ]; do
  ID=$((ID + 1))
done

# Pad ID to 3 digits
ID_PADDED=$(printf "%03d" $ID)

# Create filename
FILENAME="$ID_PADDED-$SLUG.$EXTENSION"
FILEPATH="$ROUTE/$FILENAME"

# Read template
TEMPLATE_PATH=".specify/templates/phr-template.prompt.md"
if [ ! -f "$TEMPLATE_PATH" ]; then
  TEMPLATE_PATH="templates/phr-template.prompt.md"
fi

if [ ! -f "$TEMPLATE_PATH" ]; then
  echo "Error: PHR template not found at $TEMPLATE_PATH"
  exit 1
fi

# Get current date
DATE_ISO=$(date +%Y-%m-%d)

# Get git info
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
USER=$(git config user.name 2>/dev/null || echo "unknown")

# Copy template and create file
cp "$TEMPLATE_PATH" "$FILEPATH"

# Replace basic placeholders
sed -i.bak "s/{{ID}}/$ID_PADDED/g" "$FILEPATH"
sed -i.bak "s/{{TITLE}}/$TITLE/g" "$FILEPATH"
sed -i.bak "s/{{STAGE}}/$STAGE/g" "$FILEPATH"
sed -i.bak "s/{{DATE_ISO}}/$DATE_ISO/g" "$FILEPATH"
sed -i.bak "s/{{SURFACE}}/agent/g" "$FILEPATH"
sed -i.bak "s/{{FEATURE}}/$FEATURE/g" "$FILEPATH"
sed -i.bak "s/{{BRANCH}}/$BRANCH/g" "$FILEPATH"
sed -i.bak "s/{{USER}}/$USER/g" "$FILEPATH"

# Remove backup file
rm -f "$FILEPATH.bak"

# Output result
if [ "$JSON_OUTPUT" = true ]; then
  echo "{\"id\":\"$ID_PADDED\",\"path\":\"$FILEPATH\",\"stage\":\"$STAGE\",\"title\":\"$TITLE\"}"
else
  echo "Created PHR: $FILEPATH"
  echo "  ID: $ID_PADDED"
  echo "  Stage: $STAGE"
  echo "  Title: $TITLE"
  echo ""
  echo "Next steps:"
  echo "  1. Open the file and fill remaining placeholders"
  echo "  2. Add full PROMPT_TEXT and RESPONSE_TEXT"
  echo "  3. Complete OUTCOME and EVALUATION sections"
fi

# Output absolute path for agent
echo "$PWD/$FILEPATH"
