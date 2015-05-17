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

			$('#lb-upload')
				.animate(
						{width:'600px'},
						{ duration: 400, queue: false} ,
						function(){/*animation complete*/});

			$('#upload-text')
				.fadeToggle("linear")
				.animate(
						{height:'300px'},
						{ duration: 500, queue: false},
						function(){/*animation complete*/});

			if ($('#upload-text').is(":visible")) {
				$("textarea[name='pom-code']").focus();
			}
		});

		$('span.toggle-upload-text').click(function (e) {
			e.stopImmediatePropagation();

			$('#lb-upload')
				.animate(
						{width:'300px'},
						{ duration: 300, queue: false},
						function(){/*animation complete*/});

			$('#upload-text')
				.hide()
				.animate(
						{height:'0px'},
						{ duration: 300, queue: false},
						function(){/*animation complete*/});

			$('button.toggle-upload-text')
				.fadeToggle("linear")
				.animate({ queue: true});
		});
	}

	function init() {
		initFileUpload();
		initPasteFile();
	}

	init();

});
