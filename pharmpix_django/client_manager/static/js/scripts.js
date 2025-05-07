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
    // const clientId = $(this).data('client-id');
    // Download files with selected date
    $('#downloadFilesBtn').click(function() {
        const selectedDate = $('#dateFilter').val();
        console.log('Selected date:', selectedDate);
        // const clientId = {{ client.id }};
        const clientId = $(this).data('client-id');
        console.log('Client ID:', clientId);
        if (selectedDate) {
            const url = window.downloadUrlBase.replace('placeholder', selectedDate);
            window.location.href = url;
        } else {
            alert('Please select a date to download files.');
        }
    });

    // Update download prompt when no files are found
    if ($('#fileTableBody tr').length === 1 && $('#fileTableBody td[colspan="5"]').length) {
        $('#downloadPrompt').html('<a href="#" id="triggerDownload" class="btn btn-primary btn-sm"><i class="fas fa-download"></i> Download Now</a>');
        $('#triggerDownload').click(function(e) {
            e.preventDefault();
            const selectedDate = $('#dateFilter').val();
            // const clientId = {{ client.id }};
            const clientId = $(this).data('client-id');
            if (selectedDate) {
                const url = window.downloadUrlBase.replace('placeholder', selectedDate);
                window.location.href = url;
            } else {
                alert('Please select a date to download files.');
            }
        });
    }


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
    let currentFileName = null;

    $(document).on('click', '.view-file-btn', function() {
        const fileUrl = $(this).data('file-url');
        const fileId = $(this).data('file-id');
        const fileName = $(this).closest('tr').find('td:first').text();
        const errors = $(this).data('errors');
        const isValidated = $(this).data('validated');
        const isSent = $(this).data('sent');
        const clientId = $(this).data('client-id');

        currentFileId = fileId;
        currentClientId = clientId;
        currentFileName = fileName;

        console.log('Fetching file:', fileUrl);

        errorSection.addClass('hidden');
        errorContent.text('');
        modalSendSftpBtn.hide();
        modalReplaceBtn.hide();

        if (errors) {
            errorSection.find('h4').text(`Validation Errors for ${currentFileName}`);
            errorContent.text(errors);
            errorSection.removeClass('hidden');
            const replaceUrl = window.replaceUrlBase.replace('0', fileId);
            modalReplaceBtn.attr('href', replaceUrl);
            modalReplaceBtn.show();
        } else if (isValidated && !isSent) {
            modalSendSftpBtn.show();
        }

        fetch(fileUrl, { method: 'HEAD' })
            .then(response => {
                console.log('HEAD response status:', response.status);
                const contentDisposition = response.headers.get('Content-Disposition');
                console.log('Content-Disposition:', contentDisposition);
                if (contentDisposition && contentDisposition.includes('attachment')) {
                    fileFrame.html(`
                        <p>This file type cannot be viewed directly. <a href="${fileUrl}" download><i class="fas fa-download"></i></a></p>
                    `);
                    fileModal.show();
                } else {
                    fetch(fileUrl)
                        .then(resp => {
                            if (!resp.ok) throw new Error(`HTTP error! status: ${resp.status}`);
                            return resp.text();
                        })
                        .then(content => {
                            fileFrame.text(content);
                            fileModal.show();
                            if (isValidated && !isSent) {
                                sendToSftp(fileId, clientId);
                            }
                        })
                        .catch(error => {
                            console.error('Error loading file content:', error);
                            fileFrame.html('<p>Failed to load file content. <a href="${fileUrl}" download><i class="fas fa-download"></i></a></p>');
                            fileModal.show();
                        });
                }
            })
            .catch(error => {
                console.error('Error checking file type:', error);
                fileFrame.html('<p>Failed to load file. <a href="${fileUrl}" download><i class="fas fa-download"></i></a></p>');
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
        currentFileName = null;
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
            currentFileName = null;
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


    $('.download-btn').click(function(e) {
        e.preventDefault();
        const downloadUrlBase = $(this).data('download-url');
        const selectedDate = $('#dateFilter').val();
        if (selectedDate) {
            const url = downloadUrlBase.replace('placeholder', selectedDate);
            window.location.href = url;
        } else {
            alert('Please select a date to download files.');
        }
    });
});
