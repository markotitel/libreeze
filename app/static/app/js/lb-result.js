$(function () {
	"use strict";

	var _dependencyCodeCSSClass = 'dependency-xml',
		_dependencyCollapsedCSSClass = 'dependency-collapsed',
		_dependencyRowActiveCSSClass = 'active';

	function showDependencyCode() {
		$('.view-xml').click(function () {
			// Toggle next table row containing dependency xml
			$(this).closest('tr').toggleClass(_dependencyRowActiveCSSClass);
			$(this).parent('tr').next('tr.' + _dependencyCodeCSSClass).toggleClass(_dependencyCollapsedCSSClass);
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
		var $copyButton = $(".copy-xml");

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