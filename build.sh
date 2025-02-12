#!/bin/bash

# Default to development values if environment variables aren't set
API_URL=${REACT_APP_API_URL:-'https://teacherdavid.pythonanywhere.com'}
SHEET_ID=${REACT_APP_SHEET_ID:-'1_gFP3lKUEWAvKAuXbpPT-2hRp7Mvy11TJjoAwz_ck80'}

# Create config.js with environment variables
echo "window.ENV = {
  API_URL: '$API_URL',
  SHEET_ID: '$SHEET_ID'
};" > static/config.js 