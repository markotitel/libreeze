$(function () {
	"use strict";

	function showDependencyCode() {
		$('.view-xml').click(function () {
			// Show next table row containing dependency xml
			$(this).toggleClass('active');
			$(this).parent('tr').next('tr.dependency-xml').toggleClass('hidden');
		});

		$('.hide-xml').click(function(){
			$(this).closest('tr.dependency-xml').addClass('hidden');
			$(this).closest('tr.dependency-xml').prev('tr').children('.view-xml').removeClass('active');
		});
	}

	function selectOnFocus() {
		$('.xml-result').focus(function () {
			var $this = $(this);
			$this.select();

			// Work around Chrome's little problem
			$this.mouseup(function () {
				// Prevent further mouseup intervention
				$this.unbind("mouseup");
				return false;
			});
		});
	}

	function zeroClipboard() {
		var $copyButton = $("#copy-xml");

		if ($copyButton.length === 0) {
			return false;
		}
		if (!window.ZeroClipboard) {
			return false;
		}

		var client = new ZeroClipboard($copyButton);

		client.on("ready", function () {
			client.on("aftercopy", function (event) {
				// `this` === `client`
				// `event.target` === the element that was clicked
				//event.target.style.display = "none";
				alert("Copied text to clipboard: \n" + event.data["text/plain"]);
			});
		});
	}

	function init() {
		selectOnFocus();
		zeroClipboard();
		showDependencyCode();
	}

	init();

});