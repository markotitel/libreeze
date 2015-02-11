$(function(){
    "use strict";
    
	function initFileUpload()
    {
        var $fileInput = $('input[name=pom-file]');
        
        $fileInput.change(function(){
            var form = $('#upload-file');
            console.debug('file selected; submit form');
            form.submit();
        });
        
        $('.browse-btn').click(function(){
            $fileInput.click();
        });
    }
    
    function initPasteFile()
    {
        $('.toggle-upload-text').click(function(e){
            e.stopPropagation();
            $('#upload-text').show();
            $("textarea[name='enter-code']").focus();
            $(this).hide();
        });
    }
        
    function init()
    {
        initFileUpload();
        initPasteFile();
    }
    
    init();
    
});