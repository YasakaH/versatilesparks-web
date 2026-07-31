-- Add extra top margin before chapter titles to satisfy KDP minimum of 0.375"
return {
  Header = function(h)
    if h.level == 1 then  -- Chapter headings
      table.insert(h.content, 1, pandoc.RawInline('latex', '\\vspace{0.75in}'))
    end
    return h
  end,
  
  Div = function(d)
    -- Check if this is a part div (KMPart from Quarto)
    if d.classes:includes 'KMPart' then
      table.insert(d.attributes, 'lua-header-insert=\\vspace{0.5in}')
    end
    return d
  end
}
