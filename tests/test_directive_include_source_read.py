"""Test the include directive source-read event integration."""

import pytest


@pytest.mark.sphinx('html', testroot='source-read-include')
def test_source_read_event_with_include(app):
    """Test that source-read event is applied to included content."""
    # Register source-read handler that replaces &REPLACE_ME; with REPLACED
    def source_read_handler(app, docname, source):
        source[0] = source[0].replace('&REPLACE_ME;', 'REPLACED')
    
    app.connect('source-read', source_read_handler)
    app.build()
    
    # Check that the HTML contains the replaced text for all included content
    html = (app.outdir / 'index.html').read_text(encoding='utf8')
    
    # All three instances of &REPLACE_ME; should be replaced with REPLACED
    assert 'REPLACE_ME' not in html
    assert html.count('REPLACED') == 3  # main doc + 2 included files


@pytest.mark.sphinx('html', testroot='source-read-include') 
def test_source_read_event_called_for_includes(app):
    """Test that source-read event is called for included files."""
    events_called = []
    
    def source_read_handler(app, docname, source):
        events_called.append(docname)
        source[0] = source[0].replace('&REPLACE_ME;', 'REPLACED')
    
    app.connect('source-read', source_read_handler)
    # Force a clean build to ensure source-read is called
    app.env.all_docs.clear()
    app.build()
    
    # Should be called for main document and both included files
    assert 'index' in events_called
    assert 'something-to-include' in events_called 
    assert 'subdir/sub' in events_called