// static/js/scripts.js
$(document).ready(function() {
    // Delete confirmation
    $('.delete-btn').click(function(e) {
        if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
            e.preventDefault();
        }
    });

    // Table row hover effect
    $('.client-table tr').hover(
        function() {
            $(this).css('cursor', 'pointer');
        },
        function() {
            $(this).css('cursor', 'default');
        }
    );

    // File viewer modal
    const modal = $('#fileModal');
    const fileFrame = $('#fileFrame');
    const span = $('.close');

    $('.view-file-btn').click(function() {
        const fileUrl = $(this).data('file-url');
        fileFrame.attr('src', fileUrl);
        modal.show();
    });

    span.click(function() {
        modal.hide();
        fileFrame.attr('src', '');
    });

    $(window).click(function(event) {
        if (event.target == modal[0]) {
            modal.hide();
            fileFrame.attr('src', '');
        }
    });
});