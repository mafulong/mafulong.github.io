#!/bin/bash

set -e

echo "🔍 Checking local environment..."

# Check Ruby
if ! command -v ruby &> /dev/null; then
    echo "❌ Ruby not found. Please install Ruby first."
    exit 1
fi
echo "✅ Ruby: $(ruby --version)"

# Check Gem
if ! command -v gem &> /dev/null; then
    echo "❌ Gem not found. Please install Ruby gem."
    exit 1
fi
echo "✅ Gem: $(gem --version)"

# Check Bundle
if ! command -v bundle &> /dev/null; then
    echo "⚠️  Bundle not found. Installing..."
    gem install bundler
fi
echo "✅ Bundle: $(bundle --version)"

# Install dependencies if needed
echo ""
echo "📦 Checking dependencies..."
cd "$(dirname "$0")/.."

if [ ! -f "Gemfile.lock" ] || ! bundle check &> /dev/null; then
    echo "⚠️  Dependencies not installed. Running bundle install..."
    bundle install
else
    echo "✅ Dependencies installed"
fi

# Start Jekyll server
echo ""
echo "🚀 Starting Jekyll server..."
echo "   Preview: http://127.0.0.1:4000"
echo "   Press Ctrl+C to stop"
echo ""

bundle exec jekyll serve --port 4000
