source "https://rubygems.org"

# GitHub Pages builds this site with its own pinned gem set. This Gemfile only
# has to reproduce that build locally: bundle exec jekyll serve
#
# The github-pages gem cannot install on Ruby 4 (its commonmarker dependency
# needs Ruby < 4.0), so these pins copy https://pages.github.com/versions.json
# directly. Update them when that list changes.
gem "jekyll", "3.10.0"
gem "liquid", "4.0.4"
gem "kramdown", "2.4.0"
gem "kramdown-parser-gfm", "1.1.0"

group :jekyll_plugins do
  gem "jekyll-feed", "0.17.0"
  gem "jekyll-sitemap", "1.4.0"
  gem "jekyll-redirect-from", "0.16.0"
end

# Ruby 3.4+ no longer ships these as default gems, but Jekyll 3.10 needs them.
gem "csv"
gem "logger"
gem "base64"
gem "bigdecimal"

gem "webrick", "~> 1.8"
