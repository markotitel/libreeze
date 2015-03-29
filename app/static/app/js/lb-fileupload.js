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
		$('.toggle-upload-text').click(function (e) {
			e.stopImmediatePropagation();
			$('#upload-text').toggle();
			if ($('#upload-text').is(":visible")){
				$("textarea[name='pom-code']").focus();
			}
			$('button.toggle-upload-text').toggle();
		});
	}

	function init() {
		initFileUpload();
		initPasteFile();
	}

	init();

});