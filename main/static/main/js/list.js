window.onloadFuncs.push(function () {
    let converter = new showdown.Converter();
    converter.setOption('omitExtraWLInCodeBlocks', false);
    converter.setOption('parseImgDimensions', true);
    converter.setOption('simplifiedAutoLink', true);
    converter.setOption('excludeTrailingPunctuationFromURLs', true);
    converter.setOption('strikethrough', true);
    converter.setOption('tables', true);
    converter.setOption('ghCodeBlocks', true);
    converter.setOption('tasklists', true);
    converter.setOption('smoothLivePreview', true);
    converter.setOption('smartIndentationFix', true);
    converter.setOption('simpleLineBreaks', true);
    converter.setOption('requireSpaceBeforeHeadingText', true);
    converter.setOption('encodeEmails', true);
    converter.setOption('emoji', true);
    converter.setOption('underline', true);
    converter.setOption('ghMentions', true);
    converter.setOption('ghMentionsLink', '/{u}');
    converter.setOption('ghCompatibleHeaderId ', true);

    let torenders = document.getElementsByClassName('note_digest');
    Array.from(torenders).forEach(i => {
        i.innerHTML = converter.makeHtml(i.firstElementChild.value);
    })
});