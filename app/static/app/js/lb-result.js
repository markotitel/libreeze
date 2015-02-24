$(function(){   
    "use strict";
    
    function initSelectOnFocus() 
    {
        $('.xml-result').focus(function(){
            var $this = $(this);
            $this.select();

            // Work around Chrome's little problem
            $this.mouseup(function(){
                // Prevent further mouseup intervention
                $this.unbind("mouseup");
                return false;
            });
        });
    }
        
    function initZeroClipboard() 
    {
		var $copyButton = $("#copy-button");
        
		if ($copyButton.length === 0) { return false; }		
        if (!window.ZeroClipboard){ return false; }
        
		var client = new ZeroClipboard($copyButton);

		client.on("ready", function(){
            client.on("aftercopy", function(event){
                // `this` === `client`
                // `event.target` === the element that was clicked
                event.target.style.display = "none";
                //alert("Copied text to clipboard: \n" + event.data["text/plain"]);
            });
        });
	}
    
    function init() 
    {
        initSelectOnFocus();
        initZeroClipboard();
    }
    
    init();
    
});