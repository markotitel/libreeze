$(function(){
    
	$pasteForm = $('form#paste_form');
    
    var init = function(){
		initZeroClipboard();
    };
    
    //=begin Toggle paste section
    $('.toggle_paste_form button').click(function(e){
        e.stopPropagation();
        $pasteForm.show();
		$("textarea[name='enter_code']").focus();
		$(this).hide();
    });
    //=end Toggle paste section
    
    //=begin Select input content on focus    
    $('.xml_result').focus(function(){
        var $this = $(this);
        $this.select();
        
        // Work around Chrome's little problem
        $this.mouseup(function() {
            // Prevent further mouseup intervention
            $this.unbind("mouseup");
            return false;
        });
      });
    //=end Select input content on focus
    
    // Copy to clipboard
	var initZeroClipboard = function(){
		$copyButton = $("#copy-button");
		if ($copyButton.length == 0){ return false; }
		
		var client = new ZeroClipboard( $copyButton );

		client.on( "ready", function( readyEvent ) {
		  client.on( "aftercopy", function( event ) {
			// `this` === `client`
			// `event.target` === the element that was clicked
			//event.target.style.display = "none";
			alert("Copied text to clipboard: \n" + event.data["text/plain"] );
		  } );
		} );
	};
    
    init();
    
});