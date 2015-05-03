$(function () {
	"use strict";

	function initFileUpload() {
		var $fileInput = $('input[name=pom-file]');

		$fileInput.on('change', (function () {
			var form = $('#upload-file');
			console.debug('file selected; submit form');
			form.submit();
		}));

		$('.browse-btn').click(function () {
			$fileInput.val('');
			$fileInput.click();
		});
	}

	function initPasteFile() {
		$('button.toggle-upload-text').click(function (e) {
			$(this).hide();
			e.stopImmediatePropagation();
			$('#upload-text').fadeToggle("linear");
			if ($('#upload-text').is(":visible")){
				$("textarea[name='pom-code']").focus();
			}
		});

		$('span.toggle-upload-text').click(function (e) {
			e.stopImmediatePropagation();
			$('#upload-text').hide();
			$('button.toggle-upload-text').fadeToggle("linear");
		});
	}

	function init() {
		initFileUpload();
		initPasteFile();
	}

	init();

});
