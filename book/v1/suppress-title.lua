-- Suppress automatic \maketitle for PDF.
-- Title page is handled manually via include-before-body.
function Meta(meta)
  meta['title'] = pandoc.MetaInlines({pandoc.Str('')})
  return meta
end

function Pandoc(doc)
  return doc
end
