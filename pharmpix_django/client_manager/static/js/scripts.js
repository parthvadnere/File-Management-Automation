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
    const fileModal = $('#fileModal');
    const fileFrame = $('#fileFrame');
    const errorSection = $('#errorSection');
    const errorContent = $('#errorContent');
    const modalSendSftpBtn = $('#modalSendSftpBtn');
    const modalReplaceBtn = $('#modalReplaceBtn');
    const close = $('.close');
    const errorModal = $('#errorModal');
    const standaloneErrorContent = $('#standaloneErrorContent');
    const closeError = $('.close-error');

    let currentFileId = null;
    let currentClientId = null;

    $('.view-file-btn').click(function() {
        const fileUrl = $(this).data('file-url');
        const fileId = $(this).data('file-id');
        const errors = $(this).data('errors');
        const isValidated = $(this).data('validated');
        const isSent = $(this).data('sent');
        const clientId = $(this).data('client-id');

        currentFileId = fileId;
        currentClientId = clientId;

        console.log('Fetching file:', fileUrl);

        // Reset modal state
        errorSection.addClass('hidden');
        errorContent.text('');
        modalSendSftpBtn.hide();
        modalReplaceBtn.hide();

        // Show errors if they exist
        if (errors) {
            errorContent.text(errors);
            errorSection.removeClass('hidden');
            // Show Replace button if there are errors
            // modalReplaceBtn.attr('href', `{% url 'client_manager:replace_file' 0 %}`.replace('0', fileId));
            const replaceUrl = window.replaceUrlBase.replace('0', fileId);
            modalReplaceBtn.attr('href', replaceUrl);
            modalReplaceBtn.show();
        } else if (isValidated && !isSent) {
            // If no errors and not sent, show Send to SFTP button
            modalSendSftpBtn.show();
        }

        // Fetch the file content
        fetch(fileUrl, { method: 'HEAD' })
            .then(response => {
                console.log('HEAD response status:', response.status);
                const contentDisposition = response.headers.get('Content-Disposition');
                console.log('Content-Disposition:', contentDisposition);
                if (contentDisposition && contentDisposition.includes('attachment')) {
                    fileFrame.html(`
                        <p>This file type cannot be viewed directly. <a href="${fileUrl}" download>Click here to download</a>.</p>
                    `);
                    fileModal.show();
                } else {
                    fetch(fileUrl)
                        .then(resp => {
                            console.log('GET response status:', resp.status);
                            console.log('GET response headers:', Object.fromEntries(resp.headers));
                            if (!resp.ok) throw new Error(`HTTP error! status: ${resp.status}`);
                            return resp.text();
                        })
                        .then(content => {
                            console.log('Fetched content (first 50 chars):', content.substring(0, 50));
                            fileFrame.text(content);
                            fileModal.show();

                            // If file is validated and not sent, attempt to send to SFTP automatically
                            if (isValidated && !isSent) {
                                sendToSftp(fileId, clientId);
                            }
                        })
                        .catch(error => {
                            console.error('Error loading file content:', error);
                            fileFrame.html('<p>Failed to load file content. Check console for details. Please try downloading instead.</p>');
                            fileModal.show();
                        });
                }
            })
            .catch(error => {
                console.error('Error checking file type:', error);
                fileFrame.html('<p>Failed to load file. Check console for details. Please try downloading instead.</p>');
                fileModal.show();
            });
    });

    close.click(function() {
        fileModal.hide();
        fileFrame.text('');
        errorSection.addClass('hidden');
        errorContent.text('');
        modalSendSftpBtn.hide();
        modalReplaceBtn.hide();
        currentFileId = null;
        currentClientId = null;
    });

    $(window).click(function(event) {
        if (event.target == fileModal[0]) {
            fileModal.hide();
            fileFrame.text('');
            errorSection.addClass('hidden');
            errorContent.text('');
            modalSendSftpBtn.hide();
            modalReplaceBtn.hide();
            currentFileId = null;
            currentClientId = null;
        }
        if (event.target == errorModal[0]) {
            errorModal.hide();
            standaloneErrorContent.text('');
        }
    });

    // Send to SFTP from modal
    modalSendSftpBtn.click(function() {
        if (currentFileId && currentClientId) {
            sendToSftp(currentFileId, currentClientId);
        }
    });

    // Send to SFTP from table
    $('.send-sftp-btn').click(function() {
        const fileId = $(this).data('file-id');
        const clientId = $(this).data('client-id');
        sendToSftp(fileId, clientId);
    });

    // Error modal handling
    $('.view-errors-btn').click(function() {
        const errors = $(this).data('errors');
        standaloneErrorContent.text(errors);
        errorModal.show();
    });

    closeError.click(function() {
        errorModal.hide();
        standaloneErrorContent.text('');
    });

    function sendToSftp(fileId, clientId) {
        $.ajax({
            url: '{% url "send_to_sftp" %}',
            method: 'POST',
            data: {
                file_id: fileId,
                client_id: clientId,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function(response) {
                if (response.status === 'success') {
                    alert('File sent to SFTP successfully.');
                    location.reload();
                } else {
                    alert('Failed to send file to SFTP: ' + response.message);
                }
            },
            error: function() {
                alert('Error sending file to SFTP. Please try again.');
            }
        });
    }

});
