// Function to add header with logo and system name to pages
function addPageHeader() {
// Create header container
const headerContainer = document.createElement('div');
headerContainer.className = 'header-container';

// Create logo image
const logoImg = document.createElement('img');
logoImg.src = '4.png';
logoImg.alt = '系统Logo';
logoImg.className = 'logo';

// Create system name
const systemName = document.createElement('span');
systemName.className = 'system-name';
systemName.textContent = 'ᅟᅠ        ‌‍‎‏ 北京信息科技大学体育场馆预约系统（试运行）';

// Create container for logo and system name with flex display
const logoTitleContainer = document.createElement('div');
logoTitleContainer.className = 'logo-title-container';
logoTitleContainer.style.display = 'flex';
logoTitleContainer.style.alignItems = 'center';
logoTitleContainer.style.gap = '10px';
logoTitleContainer.appendChild(logoImg);
logoTitleContainer.appendChild(systemName);

// Append to header container
headerContainer.appendChild(logoTitleContainer);

// Insert at top of body
document.body.insertBefore(headerContainer, document.body.firstChild);
}

// Execute when DOM is loaded
document.addEventListener('DOMContentLoaded', addPageHeader);
