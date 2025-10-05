// Configuration - Backend URL based on environment
const isLocal = window.location.hostname === 'localhost' || 
                window.location.hostname === '127.0.0.1' ||
                window.location.hostname === '0.0.0.0' ||
                window.location.protocol === 'file:';

const BACKEND_URL = isLocal 
    ? 'http://localhost:5000' 
    : window.location.origin;
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling to all anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
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

// Merging queue functionality
let mergingQueue = [];

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
    
    // Send files to backend
    fetch(`${BACKEND_URL}/api/process-files`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('DEBUG: Received JSON data:', data);  // Debug log
        if (data.success) {
            // Display JSON results
            showJsonResults(data.results, data.file_count, boxNumber, data.is_schema);
        } else {
            alert(`Error: ${data.error}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error processing files. Please make sure the backend server is running.');
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
    
    // Send files to backend with schema flag
    fetch(`${BACKEND_URL}/api/process-files?schema=true`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('DEBUG: Received schema JSON data:', data);  // Debug log
        if (data.success) {
            // Display JSON results
            showJsonResults(data.results, data.file_count, boxNumber, data.is_schema);
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

function showJsonResults(results, fileCount, boxNumber, isSchema) {
    console.log('DEBUG: showJsonResults called with:', results, fileCount, boxNumber, isSchema);
    
    // Create a modal for displaying JSON results
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
            <h3 style="color: #333; margin-bottom: 0.5rem;">JSON Conversion Results - ${fileTypeLabel} Box ${boxNumber}</h3>
            <p style="color: #666;">Converted ${fileCount} file(s) to JSON format</p>
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
                    <p style="color: #dc3545; font-style: italic;">${result.json_data.error}</p>
                </div>
            `;
        } else {
            const jsonData = result.json_data;
            
            if (jsonData.sheets) {
                // Multiple sheets Excel file
                resultsHTML += `
                    <div style="background: white; padding: 1rem; border-radius: 8px;">
                        <h5 style="color: #666; margin-bottom: 1rem;">📊 Excel File with ${jsonData.sheet_count} Sheet(s) - Total ${jsonData.total_rows} Rows</h5>
                        <div style="margin-bottom: 1rem;">
                            ${result.json_filename ? `
                                <button onclick="addToMergingQueue('${result.json_filename}', '${result.filename}', '${result.unique_id}')" style="
                                    background: #28a745;
                                    color: white;
                                    padding: 10px 20px;
                                    border: none;
                                    border-radius: 5px;
                                    cursor: pointer;
                                    font-weight: bold;
                                ">📋 Add to Merging Queue</button>
                            ` : ''}
                        </div>
                        ${result.json_filename ? `
                            <div style="background: #e7f3ff; padding: 10px; border-radius: 5px; margin-bottom: 10px; border-left: 3px solid #17a2b8;">
                                <p style="margin: 0; font-size: 0.9rem; color: #333;">
                                    <strong>💾 Saved to server:</strong> ${result.json_filename}<br>
                                    <strong>🔗 API URL:</strong> <code style="background: #f8f9fa; padding: 2px 4px; border-radius: 3px;">http://localhost:5000/api/json-files/${result.json_filename}</code><br>
                                    <strong>🆔 Unique ID:</strong> ${result.unique_id}
                                </p>
                            </div>
                        ` : ''}
                `;
                
                Object.entries(jsonData.sheets).forEach(([sheetName, sheetData]) => {
                    const sheetColor = sheetData.error ? '#dc3545' : '#28a745';
                    resultsHTML += `
                        <div style="margin: 1rem 0; padding: 1rem; background: #e9ecef; border-radius: 5px; border-left: 3px solid ${sheetColor};">
                            <h6 style="color: ${sheetColor}; margin-bottom: 0.5rem;">📋 ${sheetData.title}</h6>
                            <p style="color: #666; font-size: 0.9rem; margin: 0;">Sheet: ${sheetName} | Rows: ${sheetData.row_count || 0}</p>
                            ${sheetData.columns ? `<p style="color: #666; font-size: 0.8rem; margin: 0.5rem 0;">Columns: ${sheetData.columns.join(', ')}</p>` : ''}
                        </div>
                    `;
                });
                
                resultsHTML += `</div>`;
            } else {
                // Single sheet file
                const rowCount = jsonData.row_count || 0;
                resultsHTML += `
                    <div style="background: white; padding: 1rem; border-radius: 8px;">
                        <h5 style="color: #666; margin-bottom: 1rem;">📊 ${jsonData.file_type} File - ${rowCount} Rows</h5>
                        ${jsonData.title ? `<p style="color: #333; font-weight: bold; margin-bottom: 0.5rem;">${jsonData.title}</p>` : ''}
                        ${jsonData.columns ? `<p style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">Columns: ${jsonData.columns.join(', ')}</p>` : ''}
                        <div style="margin-bottom: 1rem;">
                            ${result.json_filename ? `
                                <button onclick="addToMergingQueue('${result.json_filename}', '${result.filename}', '${result.unique_id}')" style="
                                    background: #28a745;
                                    color: white;
                                    padding: 10px 20px;
                                    border: none;
                                    border-radius: 5px;
                                    cursor: pointer;
                                    font-weight: bold;
                                ">📋 Add to Merging Queue</button>
                            ` : ''}
                        </div>
                        ${result.json_filename ? `
                            <div style="background: #e7f3ff; padding: 10px; border-radius: 5px; margin-bottom: 10px; border-left: 3px solid #17a2b8;">
                                <p style="margin: 0; font-size: 0.9rem; color: #333;">
                                    <strong>💾 Saved to server:</strong> ${result.json_filename}<br>
                                    <strong>🔗 API URL:</strong> <code style="background: #f8f9fa; padding: 2px 4px; border-radius: 3px;">http://localhost:5000/api/json-files/${result.json_filename}</code><br>
                                    <strong>🆔 Unique ID:</strong> ${result.unique_id}
                                </p>
                            </div>
                        ` : ''}
                    </div>
                `;
            }
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

function addToMergingQueue(jsonFilename, originalFilename, uniqueId) {
    // Check if already in queue
    const exists = mergingQueue.find(item => item.uniqueId === uniqueId);
    if (exists) {
        alert('This file is already in the merging queue!');
        return;
    }
    
    // Add to queue
    mergingQueue.push({
        jsonFilename: jsonFilename,
        originalFilename: originalFilename,
        uniqueId: uniqueId,
        addedAt: new Date().toISOString()
    });
    
    // Update merging queue display
    updateMergingQueueDisplay();
    
    alert(`Added "${originalFilename}" to merging queue!`);
}

function removeFromMergingQueue(uniqueId) {
    mergingQueue = mergingQueue.filter(item => item.uniqueId !== uniqueId);
    updateMergingQueueDisplay();
}

function clearMergingQueue() {
    mergingQueue = [];
    updateMergingQueueDisplay();
}

function updateMergingQueueDisplay() {
    let queueDisplay = document.getElementById('mergingQueueDisplay');
    if (!queueDisplay) {
        // Create the merging queue display if it doesn't exist
        const queueContainer = document.createElement('div');
        queueContainer.id = 'mergingQueueContainer';
        queueContainer.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            border: 2px solid #28a745;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 9999;
            max-width: 300px;
            max-height: 400px;
            overflow-y: auto;
        `;
        
        queueContainer.innerHTML = `
            <h4 style="margin: 0 0 10px 0; color: #28a745; display: flex; align-items: center;">
                <span style="margin-right: 8px;">📋</span> Merging Queue
            </h4>
            <div id="mergingQueueDisplay"></div>
            <div style="margin-top: 10px; text-align: center;">
                <button onclick="startMerging()" style="
                    background: #28a745;
                    color: white;
                    padding: 8px 16px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    margin-right: 5px;
                ">🚀 Start Merging</button>
                <button onclick="clearMergingQueue()" style="
                    background: #dc3545;
                    color: white;
                    padding: 8px 16px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                ">🗑️ Clear All</button>
            </div>
        `;
        
        document.body.appendChild(queueContainer);
        queueDisplay = document.getElementById('mergingQueueDisplay');
    }
    
    if (mergingQueue.length === 0) {
        queueDisplay.innerHTML = '<p style="color: #666; font-style: italic; margin: 0;">No files in queue</p>';
        document.getElementById('mergingQueueContainer').style.display = 'none';
        return;
    }
    
    document.getElementById('mergingQueueContainer').style.display = 'block';
    
    let queueHTML = '';
    mergingQueue.forEach((item, index) => {
        queueHTML += `
            <div style="
                background: #f8f9fa;
                padding: 8px;
                border-radius: 5px;
                margin-bottom: 5px;
                border-left: 3px solid #28a745;
                display: flex;
                justify-content: space-between;
                align-items: center;
            ">
                <div style="flex: 1;">
                    <div style="font-weight: bold; font-size: 0.9rem;">${item.originalFilename}</div>
                    <div style="font-size: 0.8rem; color: #666;">${item.jsonFilename}</div>
                </div>
                <button onclick="removeFromMergingQueue('${item.uniqueId}')" style="
                    background: #dc3545;
                    color: white;
                    border: none;
                    border-radius: 3px;
                    padding: 4px 8px;
                    cursor: pointer;
                    font-size: 0.8rem;
                ">×</button>
            </div>
        `;
    });
    
    queueDisplay.innerHTML = queueHTML;
}

function startMerging() {
    if (mergingQueue.length === 0) {
        alert('No files in merging queue!');
        return;
    }
    
    // Send merging request to backend
    fetch(`${BACKEND_URL}/api/start-merging`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            files: mergingQueue
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Merging started! Check the console for results.');
            console.log('Merging results:', data);
            // Clear the queue after successful start
            clearMergingQueue();
        } else {
            alert(`Error: ${data.error}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error starting merging process. Please make sure the backend server is running.');
    });
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}