$(document).ready(function() {
    // Delete confirmation
    $('.delete-btn').click(function(e) {
        e.preventDefault();
        const href = $(this).attr('href');
        Swal.fire({
            icon: 'warning',
            title: 'Are you sure?',
            text: 'This action cannot be undone.',
            showCancelButton: true,
            confirmButtonText: 'Delete',
            cancelButtonText: 'Cancel',
            confirmButtonColor: '#dc3545',
            cancelButtonColor: '#6c757d',
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = href;
            }
        });
    });

    // Table row hover effect
    $('.config-table tr').hover(
        function() {
            $(this).css('cursor', 'pointer');
        },
        function() {
            $(this).css('cursor', 'default');
        }
    );

    // Download files with selected date
    $('#downloadFilesBtn').click(function() {
        const selectedDate = $('#dateFilter').val();
        const clientId = $(this).data('client-id');
        if (selectedDate) {
            const url = window.downloadUrlBase.replace('placeholder', selectedDate);
            window.location.href = url;
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Please select a date to download files.',
                confirmButtonText: 'OK',
                timer: 5000,
                timerProgressBar: true,
            });
        }
    });

    // Update download prompt when no files are found
    if ($('#fileTableBody tr').length === 1 && $('#fileTableBody td.no-data').length) {
        $('#downloadPrompt').html('<a href="#" id="triggerDownload" class="refresh-btn"><i class="fas fa-download"></i> Download Now</a>');
        $('#triggerDownload').click(function(e) {
            e.preventDefault();
            const selectedDate = $('#dateFilter').val();
            const clientId = $(this).data('client-id');
            if (selectedDate) {
                const url = window.downloadUrlBase.replace('placeholder', selectedDate);
                window.location.href = url;
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Please select a date to download files.',
                    confirmButtonText: 'OK',
                    timer: 5000,
                    timerProgressBar: true,
                });
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

        errorSection.addClass('hidden');
        errorContent.text('');
        modalSendSftpBtn.hide();
        modalReplaceBtn.hide();

        if (errors) {
            errorSection.find('h4').text(`Validation Errors for ${currentFileName}`);
            errorContent.text(errors);
            errorSection.removeClass('hidden');
            if (window.replaceUrlBase) {
                const replaceUrl = window.replaceUrlBase.replace('0', fileId);
                modalReplaceBtn.attr('href', replaceUrl);
                modalReplaceBtn.show();
            } else {
                console.error('window.replaceUrlBase is undefined.');
                modalReplaceBtn.hide();
            }
        } else if (isValidated && !isSent) {
            modalSendSftpBtn.show();
        }

        const isTextFile = fileName.toLowerCase().endsWith('.txt');
        if (isTextFile) {
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
                    fileFrame.html(`<p>Failed to load file content. <a href="${fileUrl}" download><i class="fas fa-download"></i> Download</a></p>`);
                    fileModal.show();
                });
        } else {
            fetch(fileUrl, { method: 'HEAD' })
                .then(response => {
                    const contentDisposition = response.headers.get('Content-Disposition');
                    if (contentDisposition && contentDisposition.includes('attachment')) {
                        fileFrame.html(`
                            <p>This file type cannot be viewed directly. <a href="${fileUrl}" download><i class="fas fa-download"></i> Download</a></p>
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
                                fileFrame.html(`<p>Failed to load file content. <a href="${fileUrl}" download><i class="fas fa-download"></i> Download</a></p>`);
                                fileModal.show();
                            });
                    }
                })
                .catch(error => {
                    console.error('Error checking file type:', error);
                    fileFrame.html(`<p>Failed to load file. <a href="${fileUrl}" download><i class="fas fa-download"></i> Download</a></p>`);
                    fileModal.show();
                });
        }
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

    modalSendSftpBtn.click(function() {
        if (currentFileId && currentClientId) {
            sendToSftp(currentFileId, currentClientId);
        }
    });

    $('.send-sftp-btn').click(function() {
        const fileId = $(this).data('file-id');
        const clientId = $(this).data('client-id');
        sendToSftp(fileId, clientId);
    });

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
                Swal.fire({
                    icon: response.status === 'success' ? 'success' : 'error',
                    title: response.status === 'success' ? 'Success' : 'Error',
                    text: response.status === 'success' ? 'File sent to SFTP successfully.' : 'Failed to send file to SFTP: ' + response.message,
                    confirmButtonText: 'OK',
                    timer: 5000,
                    timerProgressBar: true,
                }).then(() => {
                    if (response.status === 'success') {
                        location.reload();
                    }
                });
            },
            error: function() {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Error sending file to SFTP. Please try again.',
                    confirmButtonText: 'OK',
                    timer: 5000,
                    timerProgressBar: true,
                });
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
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Please select a date to download files.',
                confirmButtonText: 'OK',
                timer: 5000,
                timerProgressBar: true,
            });
        }
    });
});