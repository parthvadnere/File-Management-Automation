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
        console.log("into view file btn click");
        const fileUrl = $(this).data('file-url');
        const fileId = $(this).data('file-id');

        console.log('Fetching file:', fileUrl);

        // Fetch the file to check its Content-Disposition and content
        fetch(fileUrl, { method: 'HEAD' })
            .then(response => {
                console.log('HEAD response status:', response.status);
                const contentDisposition = response.headers.get('Content-Disposition');
                console.log('Content-Disposition:', contentDisposition);
                if (contentDisposition && contentDisposition.includes('attachment')) {
                    // For non-renderable files (e.g., .xlsx), show download message
                    fileFrame.html(`
                        <p>This file type cannot be viewed directly. <a href="${fileUrl}" download>Click here to download</a>.</p>
                    `);
                    modal.show();
                } else {
                    // For renderable files (e.g., .txt), fetch and display content
                    fetch(fileUrl)
                        .then(resp => {
                            console.log('GET response status:', resp.status);
                            console.log('GET response headers:', Object.fromEntries(resp.headers));
                            if (!resp.ok) throw new Error(`HTTP error! status: ${resp.status}`);
                            return resp.text();
                        })
                        .then(content => {
                            console.log('Fetched content:', content.substring(0, 50)); // Log first 50 chars
                            fileFrame.text(content); // Inject text content
                            modal.show();
                        })
                        .catch(error => {
                            console.error('Error loading file content:', error);
                            fileFrame.html('<p>Failed to load file content. Check console for details. Please try downloading instead.</p>');
                            modal.show();
                        });
                }
            })
            .catch(error => {
                console.error('Error checking file type:', error);
                fileFrame.html('<p>Failed to load file. Check console for details. Please try downloading instead.</p>');
                modal.show();
            });
    });

    span.click(function() {
        modal.hide();
        fileFrame.html(''); // Clear the content when closing
    });

    $(window).click(function(event) {
        if (event.target == modal[0]) {
            modal.hide();
            fileFrame.html('');
        }
    });
});