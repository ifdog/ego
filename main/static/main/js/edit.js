window.onloadFuncs.push(function () {
    // elements
    let preview = document.getElementById('edit_html');
    let previewdiv = document.getElementById('edit_html_div');
    let editor = document.getElementById('edit_md_area');
    let tags_hide_input = document.getElementById('edit_tags_input');
    let tags_list = document.getElementById('edit_tags_div');
    let grow_controls = document.getElementsByClassName('grow');
    let key_input = document.getElementById('edit_key_input');
    let key_header = document.getElementById('edit_key_header');
    let tag_input = document.getElementById('edit_addtag_input');
    let tag_data_list = document.getElementById('edit_addtag_data');
    let add_tag_bn = document.getElementById("edit_addtag_bn");
    let bn_commit = document.getElementById('edit_commit_lb');
    let bn_showhide = document.getElementById('edit_showhide_lb');
    let bn_save = document.getElementById('edit_save_lb');
    let bn_discard = document.getElementById('edit_discard_lb');
    let edit_form = document.getElementById('edit_form');


// 添加一个tag
    function addTag(text) {
        let bn = document.createElement('span');
        for (let i = 0; i < tags_list.children.length; i++) {
            if (tags_list.children[i].innerText === text) {
                tags_list.removeChild(tags_list.children[i]);
                break;
            }
        }
        bn.className = 'button is-warning';
        bn.innerText = text;
        bn.onclick = e => {
            tags_list.removeChild(e.target);
        };
        tags_list.appendChild(bn);
    }

    //textarea auto size
    autosize(grow_controls);
    //render markdown on load
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

    preview.innerHTML =  converter.makeHtml(editor.value);
    //init tags
    if (tags_hide_input.value) {
        tags_hide_input.value.split(',').map(i => addTag(i))
    }
    //register render markdown on input
    
    editor.oninput = () => preview.innerHTML =  converter.makeHtml(editor.value);

    //ajax on tag input
    tag_input.oninput = function () {
        let value = tag_input.value;
        if (!value) return;
        let request = new XMLHttpRequest();
        request.onreadystatechange = function (response) {
            if (request.readyState === 4 && request.status === 200) {
                tag_data_list.innerHTML = '';
                let jsonOptions = JSON.parse(request.responseText);
                jsonOptions.tags.forEach(i => {
                    let option = document.createElement('option');
                    option.value = i;
                    tag_data_list.appendChild(option);
                });
            }
        };
        request.open('GET', '/tags/query?text=' + value, true);
        request.send();

    };
    //add tags
    add_tag_bn.onclick = function () {
        let value = tag_input.value;
        if (value === "") {
            return;
        }
        addTag(value);
        tag_input.value = '';
    };

    bn_commit.onclick = () => {
        let key = key_header.innerText;
        key_input.value = key;
        tags_hide_input.value = Array.from(tags_list.children).map(i => i.innerText.trim()).join(',');
        edit_form.action = '/'+ key +'/commit'
        edit_form.submit();
    };

    bn_save.onclick = () => {
        let key = key_header.innerText;
        key_input.value = key;
        tags_hide_input.value = Array.from(tags_list.children).map(i => i.innerText.trim()).join(',');
        edit_form.action = '/'+ key +'/save'
        edit_form.submit();
    };

    bn_discard.onclick = () => {
        let key = key_header.innerText;
        key_input.value = key;
        tags_hide_input.value = Array.from(tags_list.children).map(i => i.innerText.trim()).join(',');
        edit_form.action = '/'+ key +'/discard'
        edit_form.submit();
    };

    //处理tab
    editor.onkeydown = function (e) {
        if (e.key === 'Tab') {
            console.log("tb")

            e.preventDefault();
            let s = this.selectionStart;
            this.value = this.value.substring(0, this.selectionStart) + "\t" + this.value.substring(this.selectionEnd);
            this.selectionEnd = s + 1;
        }
    }

    bn_showhide.onclick = () => {
        if(previewdiv.style.display==='none'){
            previewdiv.style.display ='block';
            bn_showhide.innerText = 'Hide';
        }else{
            previewdiv.style.display ='none';
            bn_showhide.innerText = 'Show';
        }




    };

});

