// Configuration - Backend URL based on environment
const isLocal = window.location.hostname === 'localhost' || 
                window.location.hostname === '127.0.0.1' ||
                window.location.hostname === '0.0.0.0' ||
                window.location.protocol === 'file:';

const BACKEND_URL = isLocal 
    ? 'http://localhost:5001' 
    : window.location.origin;

// Debug logging
console.log('🔧 Bridgette Frontend Configuration:');
console.log('  - isLocal:', isLocal);
console.log('  - BACKEND_URL:', BACKEND_URL);
console.log('  - window.location:', window.location.href);
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling to all anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            // const targetSection = document.querySelector(targetId);
            
            // if (targetSection) {
            //     targetSection.scrollIntoView({
            //         behavior: 'smooth',
            //         block: 'start'
            //     });
            // }
        });
    });
    
    // Add active class to navigation links based on scroll position
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-links a');
    
    window.addEventListener('scroll', function() {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (scrollY >= (sectionTop - 200)) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active');
            }
        });
    });
    
    // Handle contact form submission
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const name = this.querySelector('input[type="text"]').value;
            const email = this.querySelector('input[type="email"]').value;
            const message = this.querySelector('textarea').value;
            
            // Simple validation
            if (!name || !email || !message) {
                alert('Please fill in all fields.');
                return;
            }
            
            // Simulate form submission
            const submitButton = this.querySelector('button');
            const originalText = submitButton.textContent;
            
            submitButton.textContent = 'Sending...';
            submitButton.disabled = true;
            
            setTimeout(() => {
                alert('Thank you for your message! We\'ll get back to you soon.');
                this.reset();
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            }, 1500);
        });
    }
    
    // Add scroll effect to header
    const header = document.querySelector('header');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            header.style.background = 'rgba(102, 126, 234, 0.95)';
            header.style.backdropFilter = 'blur(10px)';
        } else {
            header.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
            header.style.backdropFilter = 'none';
        }
    });
    
    // Add animation to service cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe service cards
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
});

// Function to scroll to a specific section (used by CTA button)
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        // Get header height more reliably
        const header = document.querySelector('header');
        const headerHeight = header ? header.offsetHeight : 80;
        
        // Calculate the exact position with minimal offset
        const sectionTop = section.offsetTop - headerHeight - 10; // Reduced to just 10px spacing
        
        // Ensure we don't scroll to negative position
        const scrollPosition = Math.max(0, sectionTop);
        
        window.scrollTo({
            top: scrollPosition,
            behavior: 'smooth'
        });
        
        // Add a visual indicator that we've reached the section
        setTimeout(() => {
            section.style.outline = '3px solid rgba(102, 126, 234, 0.5)';
            section.style.outlineOffset = '10px';
            section.style.borderRadius = '10px';
            
            setTimeout(() => {
                section.style.outline = 'none';
                section.style.outlineOffset = '0';
            }, 2000);
        }, 500);
    }
}

// Add some interactive features
document.addEventListener('DOMContentLoaded', function() {
    // Add hover effect to CTA button
    const ctaButton = document.querySelector('.cta-button');
    if (ctaButton) {
        ctaButton.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.05)';
        });
        
        ctaButton.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    }
    
    // Add typing effect to hero title
    const heroTitle = document.querySelector('.hero-content h2');
    if (heroTitle) {
        const text = heroTitle.textContent;
        heroTitle.textContent = '';
        
        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                heroTitle.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        };
        
        setTimeout(typeWriter, 500);
    }
    
    // Initialize file upload functionality
    initializeFileUpload();
});

// File upload functionality
let selectedFiles1 = [];
let selectedFiles2 = [];
let selectedSchemaFiles1 = [];
let selectedSchemaFiles2 = [];

// Merge widget functionality
let uploadedFiles = {
    bank1: [],
    bank2: []
};

// Merging queue functionality removed - files processed directly by main.py

function initializeFileUpload() {
    // Initialize regular upload boxes
    initializeUploadBox(1);
    initializeUploadBox(2);
    
    // Initialize schema upload boxes
    initializeSchemaUploadBox(1);
    initializeSchemaUploadBox(2);
}

function initializeUploadBox(boxNumber) {
    const uploadBox = document.getElementById(`uploadBox${boxNumber}`);
    const fileInput = document.getElementById(`fileInput${boxNumber}`);
    
    if (!uploadBox || !fileInput) return;
    
    // Click to upload
    uploadBox.addEventListener('click', function() {
        fileInput.click();
    });
    
    // File input change
    fileInput.addEventListener('change', function(e) {
        handleFiles(e.target.files, boxNumber);
    });
    
    // Drag and drop functionality
    uploadBox.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadBox.classList.add('dragover');
    });
    
    uploadBox.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadBox.classList.remove('dragover');
    });
    
    uploadBox.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadBox.classList.remove('dragover');
        handleFiles(e.dataTransfer.files, boxNumber);
    });
}

function initializeSchemaUploadBox(boxNumber) {
    const uploadBox = document.getElementById(`schemaUploadBox${boxNumber}`);
    const fileInput = document.getElementById(`schemaFileInput${boxNumber}`);
    
    if (!uploadBox || !fileInput) return;
    
    // Click to upload
    uploadBox.addEventListener('click', function() {
        fileInput.click();
    });
    
    // File input change
    fileInput.addEventListener('change', function(e) {
        handleSchemaFiles(e.target.files, boxNumber);
    });
    
    // Drag and drop functionality
    uploadBox.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadBox.classList.add('dragover');
    });
    
    uploadBox.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadBox.classList.remove('dragover');
    });
    
    uploadBox.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadBox.classList.remove('dragover');
        handleSchemaFiles(e.dataTransfer.files, boxNumber);
    });
}

function handleFiles(files, boxNumber) {
    const selectedFiles = boxNumber === 1 ? selectedFiles1 : selectedFiles2;
    
    Array.from(files).forEach(file => {
        // Check file size (50MB limit)
        if (file.size > 50 * 1024 * 1024) {
            alert(`File "${file.name}" is too large. Maximum size is 50MB.`);
            return;
        }
        
        // Check file type
        const allowedTypes = ['.csv', '.xlsx', '.xls'];
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        
        if (!allowedTypes.includes(fileExtension)) {
            alert(`File "${file.name}" is not supported. Please upload CSV or Excel files only.`);
            return;
        }
        
        // Add file to selected files
        selectedFiles.push(file);
    });
    
    updateFileList(boxNumber);
}

function handleSchemaFiles(files, boxNumber) {
    const selectedFiles = boxNumber === 1 ? selectedSchemaFiles1 : selectedSchemaFiles2;
    
    Array.from(files).forEach(file => {
        // Check file size (50MB limit)
        if (file.size > 50 * 1024 * 1024) {
            alert(`File "${file.name}" is too large. Maximum size is 50MB.`);
            return;
        }
        
        // Check file type
        const allowedTypes = ['.csv', '.xlsx', '.xls'];
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        
        if (!allowedTypes.includes(fileExtension)) {
            alert(`File "${file.name}" is not supported. Please upload CSV or Excel files only.`);
            return;
        }
        
        // Add file to selected files
        selectedFiles.push(file);
    });
    
    updateSchemaFileList(boxNumber);
}

function updateFileList(boxNumber) {
    const selectedFiles = boxNumber === 1 ? selectedFiles1 : selectedFiles2;
    const fileList = document.getElementById(`fileList${boxNumber}`);
    const fileItems = document.getElementById(`fileItems${boxNumber}`);
    const uploadActions = document.getElementById(`uploadActions${boxNumber}`);
    
    if (!fileList || !fileItems || !uploadActions) return;
    
    if (selectedFiles.length > 0) {
        fileList.style.display = 'block';
        uploadActions.style.display = 'flex';
        
        fileItems.innerHTML = '';
        selectedFiles.forEach((file, index) => {
            const li = document.createElement('li');
            li.className = 'file-item';
            li.innerHTML = `
                <div>
                    <div class="file-name">${file.name}</div>
                    <div class="file-size">${formatFileSize(file.size)}</div>
                </div>
                <button class="remove-file" onclick="removeFile(${index}, ${boxNumber})">×</button>
            `;
            fileItems.appendChild(li);
        });
    } else {
        fileList.style.display = 'none';
        uploadActions.style.display = 'none';
    }
}

function updateSchemaFileList(boxNumber) {
    const selectedFiles = boxNumber === 1 ? selectedSchemaFiles1 : selectedSchemaFiles2;
    const fileList = document.getElementById(`schemaFileList${boxNumber}`);
    const fileItems = document.getElementById(`schemaFileItems${boxNumber}`);
    const uploadActions = document.getElementById(`schemaUploadActions${boxNumber}`);
    
    if (!fileList || !fileItems || !uploadActions) return;
    
    if (selectedFiles.length > 0) {
        fileList.style.display = 'block';
        uploadActions.style.display = 'flex';
        
        fileItems.innerHTML = '';
        selectedFiles.forEach((file, index) => {
            const li = document.createElement('li');
            li.className = 'file-item';
            li.innerHTML = `
                <div>
                    <div class="file-name">${file.name}</div>
                    <div class="file-size">${formatFileSize(file.size)}</div>
                </div>
                <button class="remove-file" onclick="removeSchemaFile(${index}, ${boxNumber})">×</button>
            `;
            fileItems.appendChild(li);
        });
    } else {
        fileList.style.display = 'none';
        uploadActions.style.display = 'none';
    }
}

function removeFile(index, boxNumber) {
    const selectedFiles = boxNumber === 1 ? selectedFiles1 : selectedFiles2;
    selectedFiles.splice(index, 1);
    updateFileList(boxNumber);
}

function clearFiles(boxNumber) {
    const selectedFiles = boxNumber === 1 ? selectedFiles1 : selectedFiles2;
    selectedFiles.length = 0; // Clear the array
    updateFileList(boxNumber);
    const fileInput = document.getElementById(`fileInput${boxNumber}`);
    if (fileInput) fileInput.value = '';
}

function removeSchemaFile(index, boxNumber) {
    const selectedFiles = boxNumber === 1 ? selectedSchemaFiles1 : selectedSchemaFiles2;
    selectedFiles.splice(index, 1);
    updateSchemaFileList(boxNumber);
}

function clearSchemaFiles(boxNumber) {
    const selectedFiles = boxNumber === 1 ? selectedSchemaFiles1 : selectedSchemaFiles2;
    selectedFiles.length = 0; // Clear the array
    updateSchemaFileList(boxNumber);
    const fileInput = document.getElementById(`schemaFileInput${boxNumber}`);
    if (fileInput) fileInput.value = '';
}

function downloadFiles() {
    fetch(`${BACKEND_URL}/api/download-files`, {
        method: 'POST',
    })
    .then(response => {
        console.log('📡 Response status:', response.status);
        console.log('📡 Response headers:', response.headers);
        
    })
}

function processFiles(boxNumber) {
    const selectedFiles = boxNumber === 1 ? selectedFiles1 : selectedFiles2;
    
    if (selectedFiles.length === 0) {
        alert('Please select files to process.');
        return;
    }
    
    // No file count restriction - can upload any number of files
    
    const processBtn = document.querySelector(`#uploadActions${boxNumber} .process-btn`);
    if (!processBtn) return;
    
    const originalText = processBtn.textContent;
    
    processBtn.textContent = 'Processing...';
    processBtn.disabled = true;
    
    // Create FormData to send files to backend
    const formData = new FormData();
    selectedFiles.forEach(file => {
        formData.append('files', file);
    });
    
    // Send files to backend with box number
    console.log('🚀 Sending request to:', `${BACKEND_URL}/api/process-files?box=${boxNumber}`);
    fetch(`${BACKEND_URL}/api/process-files?box=${boxNumber}`, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        console.log('📡 Response status:', response.status);
        console.log('📡 Response headers:', response.headers);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('✅ Received JSON data:', data);  // Debug log
        if (data.success) {
            // Display JSON results
            showFileStorageResults(data.results, data.file_count, boxNumber, data.is_schema);
        } else {
            alert(`Error: ${data.error}`);
        }
    })
    .catch(error => {
        console.error('❌ Fetch error:', error);
        alert(`Error processing files: ${error.message}\n\nPlease make sure the backend server is running on ${BACKEND_URL}`);
    })
    .finally(() => {
        processBtn.textContent = originalText;
        processBtn.disabled = false;
    });
}

function processSchemaFiles(boxNumber) {
    const selectedFiles = boxNumber === 1 ? selectedSchemaFiles1 : selectedSchemaFiles2;
    
    if (selectedFiles.length === 0) {
        alert('Please select schema files to process.');
        return;
    }
    
    const processBtn = document.querySelector(`#schemaUploadActions${boxNumber} .process-btn`);
    if (!processBtn) return;
    
    const originalText = processBtn.textContent;
    
    processBtn.textContent = 'Processing...';
    processBtn.disabled = true;
    
    // Create FormData to send files to backend
    const formData = new FormData();
    selectedFiles.forEach(file => {
        formData.append('files', file);
    });
    
    // Send files to backend with schema flag and box number
    fetch(`${BACKEND_URL}/api/process-files?schema=true&box=${boxNumber}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('DEBUG: Received schema JSON data:', data);  // Debug log
        if (data.success) {
            // Display JSON results
            showFileStorageResults(data.results, data.file_count, boxNumber, data.is_schema);
        } else {
            alert(`Error: ${data.error}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error processing schema files. Please make sure the backend server is running.');
    })
    .finally(() => {
        processBtn.textContent = originalText;
        processBtn.disabled = false;
    });
}

function showResults(results, fileCount, boxNumber) {
    console.log('DEBUG: showResults called with:', results, fileCount, boxNumber);  // Debug log
    
    // Create a modal or display area for results
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
    `;
    
    const modalContent = document.createElement('div');
    modalContent.style.cssText = `
        background: white;
        padding: 2rem;
        border-radius: 15px;
        max-width: 90%;
        max-height: 90%;
        overflow-y: auto;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    `;
    
    // Build the results HTML
    let resultsHTML = `
        <div style="text-align: center; margin-bottom: 2rem;">
            <h3 style="color: #333; margin-bottom: 0.5rem;">File Processing Results - Upload Box ${boxNumber}</h3>
            <p style="color: #666;">Processed ${fileCount} file(s)</p>
        </div>
    `;
    
    results.forEach((result, index) => {
        const fileColor = result.error ? '#dc3545' : '#28a745';
        resultsHTML += `
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem; border-left: 4px solid ${fileColor};">
                <h4 style="color: #333; margin-bottom: 1rem; display: flex; align-items: center;">
                    <span style="background: ${fileColor}; color: white; padding: 4px 8px; border-radius: 4px; margin-right: 10px; font-size: 0.8rem;">File ${index + 1}</span>
                    ${result.filename}
                </h4>
                <div style="background: white; padding: 1rem; border-radius: 8px;">
                    <h5 style="color: #666; margin-bottom: 0.5rem;">First Three Lines:</h5>
        `;
        
        if (result.error) {
            resultsHTML += `<p style="color: #dc3545; font-style: italic;">${result.data.single_tab.lines[0]}</p>`;
        } else {
            result.data.single_tab.lines.forEach((line, lineIndex) => {
                resultsHTML += `
                    <div style="margin-bottom: 0.5rem; padding: 0.5rem; background: #e9ecef; border-radius: 4px;">
                        <strong style="color: #667eea;">Line ${lineIndex + 1}:</strong> 
                        <span style="color: #333; word-wrap: break-word;">${line}</span>
                    </div>
                `;
            });
        }
        
        resultsHTML += `
                </div>
            </div>
        `;
    });
    
    resultsHTML += `
        <div style="text-align: center;">
            <button onclick="this.closest('.modal').remove()" style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 25px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
            ">Close</button>
        </div>
    `;
    
    modalContent.innerHTML = resultsHTML;
    modal.className = 'modal';
    modal.appendChild(modalContent);
    document.body.appendChild(modal);
    
    // Clear files after showing results
    clearFiles(boxNumber);
}

function showSchemaResults(results, fileCount, boxNumber) {
    console.log('DEBUG: showSchemaResults called with:', results, fileCount, boxNumber);  // Debug log
    
    // Create a modal or display area for results
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
    `;
    
    const modalContent = document.createElement('div');
    modalContent.style.cssText = `
        background: white;
        padding: 2rem;
        border-radius: 15px;
        max-width: 90%;
        max-height: 90%;
        overflow-y: auto;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    `;
    
    // Build the results HTML
    let resultsHTML = `
        <div style="text-align: center; margin-bottom: 2rem;">
            <h3 style="color: #28a745; margin-bottom: 0.5rem;">Schema Processing Results - Schema Box ${boxNumber}</h3>
            <p style="color: #666;">Processed ${fileCount} schema file(s) (starting from line 5)</p>
        </div>
    `;
    
    results.forEach((result, index) => {
        const fileColor = result.error ? '#dc3545' : '#28a745';
        resultsHTML += `
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem; border-left: 4px solid ${fileColor};">
                <h4 style="color: #333; margin-bottom: 1rem; display: flex; align-items: center;">
                    <span style="background: ${fileColor}; color: white; padding: 4px 8px; border-radius: 4px; margin-right: 10px; font-size: 0.8rem;">Schema ${index + 1}</span>
                    ${result.filename}
                </h4>
        `;
        
        if (result.error) {
            resultsHTML += `
                <div style="background: white; padding: 1rem; border-radius: 8px;">
                    <p style="color: #dc3545; font-style: italic;">${result.data.single_tab.lines[0]}</p>
                </div>
            `;
        } else {
            // Check if it's a multi-tab Excel file or single tab
            if (result.data.multiple_tabs) {
                // Multi-tab Excel file
                resultsHTML += `<h5 style="color: #666; margin-bottom: 1rem;">Multiple Tabs Found:</h5>`;
                
                Object.entries(result.data.multiple_tabs).forEach(([tabName, tabData]) => {
                    resultsHTML += `
                        <div style="background: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border: 1px solid #dee2e6;">
                            <h6 style="color: #28a745; margin-bottom: 0.5rem; font-weight: bold;">📋 ${tabData.title}</h6>
                            <p style="color: #666; font-size: 0.9rem; margin-bottom: 0.5rem;">Tab: ${tabName}</p>
                            <div style="margin-top: 0.5rem;">
                    `;
                    
                    tabData.lines.forEach((line, lineIndex) => {
                        resultsHTML += `
                            <div style="margin-bottom: 0.3rem; padding: 0.3rem 0.5rem; background: #e9ecef; border-radius: 3px; font-size: 0.9rem;">
                                <strong style="color: #28a745;">Line ${lineIndex + 5}:</strong> 
                                <span style="color: #333; word-wrap: break-word;">${line}</span>
                            </div>
                        `;
                    });
                    
                    resultsHTML += `
                            </div>
                        </div>
                    `;
                });
            } else {
                // Single tab file (CSV or single Excel sheet)
                resultsHTML += `
                    <div style="background: white; padding: 1rem; border-radius: 8px;">
                        <h5 style="color: #666; margin-bottom: 0.5rem;">First Three Lines (from line 5):</h5>
                `;
                
                result.data.single_tab.lines.forEach((line, lineIndex) => {
                    resultsHTML += `
                        <div style="margin-bottom: 0.5rem; padding: 0.5rem; background: #e9ecef; border-radius: 4px;">
                            <strong style="color: #28a745;">Line ${lineIndex + 5}:</strong> 
                            <span style="color: #333; word-wrap: break-word;">${line}</span>
                        </div>
                    `;
                });
                
                resultsHTML += `</div>`;
            }
        }
        
        resultsHTML += `</div>`;
    });
    
    resultsHTML += `
        <div style="text-align: center;">
            <button onclick="this.closest('.modal').remove()" style="
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 25px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
            ">Close</button>
        </div>
    `;
    
    modalContent.innerHTML = resultsHTML;
    modal.className = 'modal';
    modal.appendChild(modalContent);
    document.body.appendChild(modal);
    
    // Clear schema files after showing results
    clearSchemaFiles(boxNumber);
}

function showFileStorageResults(results, fileCount, boxNumber, isSchema) {
    console.log('DEBUG: showFileStorageResults called with:', results, fileCount, boxNumber, isSchema);
    
    // Update the merge widget with uploaded files
    updateMergeWidget(results, boxNumber);
    
    // Create a modal for displaying file storage results
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
    `;
    
    const modalContent = document.createElement('div');
    modalContent.style.cssText = `
        background: white;
        padding: 2rem;
        border-radius: 15px;
        max-width: 95%;
        max-height: 95%;
        overflow-y: auto;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    `;
    
    // Build the results HTML
    const fileTypeLabel = isSchema ? 'Schema' : 'Data';
    let resultsHTML = `
        <div style="text-align: center; margin-bottom: 2rem;">
            <h3 style="color: #333; margin-bottom: 0.5rem;">File Storage Results - ${fileTypeLabel} Box ${boxNumber}</h3>
            <p style="color: #666;">Saved ${fileCount} file(s) for main.py access</p>
        </div>
    `;
    
    results.forEach((result, index) => {
        const fileColor = result.error ? '#dc3545' : (isSchema ? '#28a745' : '#667eea');
        const icon = result.error ? '❌' : (isSchema ? '📋' : '📊');
        
        resultsHTML += `
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem; border-left: 4px solid ${fileColor};">
                <h4 style="color: #333; margin-bottom: 1rem; display: flex; align-items: center;">
                    <span style="background: ${fileColor}; color: white; padding: 4px 8px; border-radius: 4px; margin-right: 10px; font-size: 0.8rem;">${icon} File ${index + 1}</span>
                    ${result.filename}
                </h4>
        `;
        
        if (result.error) {
            resultsHTML += `
                <div style="background: white; padding: 1rem; border-radius: 8px;">
                    <p style="color: #dc3545; font-style: italic;">${result.message}</p>
                </div>
            `;
        } else {
            // File successfully saved
            resultsHTML += `
                <div style="background: white; padding: 1rem; border-radius: 8px;">
                    <h5 style="color: #666; margin-bottom: 1rem;">📁 File Saved Successfully</h5>
                    <div style="margin-bottom: 1rem;">
                        <!-- Merging queue removed - files processed directly by main.py -->
                    </div>
                    <div style="background: #e7f3ff; padding: 10px; border-radius: 5px; margin-bottom: 10px; border-left: 3px solid #17a2b8;">
                        <p style="margin: 0; font-size: 0.9rem; color: #333;">
                            <strong>💾 Saved as:</strong> ${result.saved_filename}<br>
                            <strong>📁 Location:</strong> uploaded_files/${result.subdirectory}/<br>
                            <strong>📊 File Type:</strong> ${result.file_type}<br>
                            <strong>📏 File Size:</strong> ${(result.file_size / 1024).toFixed(1)} KB<br>
                            <strong>🆔 Unique ID:</strong> ${result.unique_id}
                        </p>
                    </div>
                </div>
            `;
        }
        
        resultsHTML += `</div>`;
    });
    
    resultsHTML += `
        <div style="text-align: center;">
            <button onclick="this.closest('.modal').remove()" style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 25px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
            ">Close</button>
        </div>
    `;
    
    modalContent.innerHTML = resultsHTML;
    modal.className = 'modal';
    modal.appendChild(modalContent);
    document.body.appendChild(modal);
    
    // Clear files after showing results
    if (isSchema) {
        clearSchemaFiles(boxNumber);
    } else {
        clearFiles(boxNumber);
    }
}

// Removed all merging queue functions - files processed directly by main.py

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Merge Widget Functions
function updateMergeWidget(results, boxNumber) {
    const bankKey = `bank${boxNumber}`;
    
    // Add new files to the appropriate bank
    results.forEach(result => {
        if (result.error === false) {
            const fileInfo = {
                filename: result.filename,
                saved_filename: result.saved_filename,
                file_size: result.file_size,
                file_type: result.file_type,
                unique_id: result.unique_id,
                subdirectory: result.subdirectory
            };
            
            // Check if file already exists (avoid duplicates)
            const exists = uploadedFiles[bankKey].find(f => f.unique_id === result.unique_id);
            if (!exists) {
                uploadedFiles[bankKey].push(fileInfo);
            }
        }
    });
    
    // Update the display
    updateMergeWidgetDisplay();
}

function updateMergeWidgetDisplay() {
    const bank1List = document.getElementById('bank1FilesList');
    const bank2List = document.getElementById('bank2FilesList');
    const mergeActions = document.getElementById('mergeActions');
    
    // Update Bank 1 files
    if (uploadedFiles.bank1.length === 0) {
        bank1List.innerHTML = '<p class="no-files">No files uploaded yet</p>';
    } else {
        bank1List.innerHTML = uploadedFiles.bank1.map(file => `
            <div class="file-item">
                <div class="file-info">
                    <div class="file-name">${file.filename}</div>
                    <div class="file-details">${formatFileSize(file.file_size)} • ${file.file_type}</div>
                </div>
            </div>
        `).join('');
    }
    
    // Update Bank 2 files
    if (uploadedFiles.bank2.length === 0) {
        bank2List.innerHTML = '<p class="no-files">No files uploaded yet</p>';
    } else {
        bank2List.innerHTML = uploadedFiles.bank2.map(file => `
            <div class="file-item">
                <div class="file-info">
                    <div class="file-name">${file.filename}</div>
                    <div class="file-details">${formatFileSize(file.file_size)} • ${file.file_type}</div>
                </div>
            </div>
        `).join('');
    }
    
    // Show merge button if both banks have files
    if (uploadedFiles.bank1.length > 0 && uploadedFiles.bank2.length > 0) {
        mergeActions.style.display = 'block';
    } else {
        mergeActions.style.display = 'none';
    }
}

async function startMerge() {
    const mergeBtn = document.getElementById('mergeBtn');
    const mergeStatus = document.getElementById('mergeStatus');
    const mergeResults = document.getElementById('mergeResults');
    
    // Show loading state
    mergeBtn.disabled = true;
    mergeStatus.style.display = 'flex';
    
    try {
        // Call the backend merge endpoint
        const response = await fetch(`${BACKEND_URL}/api/trigger-main-processing`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Show success results
            mergeStatus.style.display = 'none';
            mergeResults.style.display = 'block';
            
            // Create download link for Excel file
            const downloadLink = document.getElementById('downloadLink');
            
            if (data.excel_file_name) {
                // Download the actual Excel file from backend
                downloadLink.href = `${BACKEND_URL}/api/download-excel/${data.excel_file_name}`;
                downloadLink.download = data.excel_file_name;
                downloadLink.style.display = 'inline-block';
            } else {
                // Fallback to JSON download if no Excel file
                const mergedData = createMergedDownloadData(data);
                const blob = new Blob([JSON.stringify(mergedData, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                
                downloadLink.href = url;
                downloadLink.download = `merged_bank_data_${new Date().toISOString().split('T')[0]}.json`;
            }
            
            // Show merge info
            document.getElementById('mergeInfo').innerHTML = `
                <strong>Files Processed:</strong> ${data.files_processed}<br>
                <strong>Total Schemas:</strong> ${data.total_schemas}<br>
                <strong>Excel File:</strong> ${data.excel_file_name || 'Not created'}<br>
                <strong>Output Directory:</strong> ${data.output_directory}
            `;
            
            console.log('✅ Merge completed successfully:', data);
            
        } else {
            throw new Error(data.error || 'Merge failed');
        }
        
    } catch (error) {
        console.error('❌ Merge error:', error);
        alert(`Error during merge: ${error.message}`);
        
        // Hide loading state
        mergeStatus.style.display = 'none';
        mergeBtn.disabled = false;
    }
}

function createMergedDownloadData(apiData) {
    return {
        merge_timestamp: new Date().toISOString(),
        summary: {
            files_processed: apiData.files_processed,
            total_schemas: apiData.total_schemas,
            json_files_created: apiData.json_files_created.length
        },
        bank1_files: uploadedFiles.bank1,
        bank2_files: uploadedFiles.bank2,
        processing_results: apiData.results,
        schema_counts: apiData.schema_counts,
        output_directory: apiData.output_directory
    };
}

async function cleanupAllFiles() {
    const cleanupBtn = document.getElementById('cleanupBtn');
    
    // Show loading state
    const originalText = cleanupBtn.innerHTML;
    cleanupBtn.innerHTML = '🔄 Cleaning...';
    cleanupBtn.disabled = true;
    
    try {
        const response = await fetch(`${BACKEND_URL}/api/cleanup-json-files`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.success || data.total_cleaned > 0) {
            // Clear the uploaded files from the frontend display
            uploadedFiles.bank1 = [];
            uploadedFiles.bank2 = [];
            updateMergeWidgetDisplay();
            
            // Show success message with details
            let message = `✅ Cleanup completed!\n\nCleaned ${data.total_cleaned} files:\n${data.cleaned_files.join('\n')}`;
            
            if (data.failed_files && data.failed_files.length > 0) {
                message += `\n\n❌ Failed to clean ${data.total_failed} files:\n${data.failed_files.join('\n')}`;
                message += `\n\n💡 These files are likely being used by the application. Try stopping and restarting the servers if needed.`;
            }
            
            alert(message);
            console.log('✅ Cleanup completed:', data.message);
        } else {
            throw new Error(data.error || 'Cleanup failed');
        }
        
    } catch (error) {
        console.error('❌ Cleanup error:', error);
        alert(`Error during cleanup: ${error.message}`);
    } finally {
        // Restore button state
        cleanupBtn.innerHTML = originalText;
        cleanupBtn.disabled = false;
    }
}