document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const closeMenu = document.getElementById('closeMenu');
    const departmentMenu = document.getElementById('departmentMenu');

    menuToggle.addEventListener('click', function() {
        departmentMenu.classList.add('active');
    });

    closeMenu.addEventListener('click', function() {
        departmentMenu.classList.remove('active');
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!menuToggle.contains(e.target) && 
            !departmentMenu.contains(e.target)) {
            departmentMenu.classList.remove('active');
        }
    });

    // Prevent menu from closing when clicking inside
    departmentMenu.addEventListener('click', function(e) {
        e.stopPropagation();
    });

    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    let debounceTimer;

    searchInput.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        const searchTerm = this.value.trim();
        
        if (searchTerm.length < 2) {
            searchResults.innerHTML = '';
            searchResults.style.display = 'none';
            return;
        }

        debounceTimer = setTimeout(() => {
            fetch(`/search_students/?term=${encodeURIComponent(searchTerm)}`)
                .then(response => response.json())
                .then(data => {
                    searchResults.innerHTML = '';
                    
                    if (data.results.length) {
                        // Group students by level
                        const studentsByLevel = {
                            '100': [],
                            '200': [],
                            '300': []
                        };
                        
                        data.results.forEach(student => {
                            studentsByLevel[student.level].push(student);
                        });
                        
                        // Create level sections
                        Object.keys(studentsByLevel).forEach(level => {
                            if (studentsByLevel[level].length > 0) {
                                const levelSection = document.createElement('div');
                                levelSection.className = 'level-section';
                                
                                levelSection.innerHTML = `
                                    <div class="level-header">
                                        <span class="level-tag">${level}L</span>
                                        <button class="select-all-btn" data-level="${level}">SELECT ALL</button>
                                    </div>
                                    <div class="student-list">
                                        ${studentsByLevel[level].map(student => `
                                            <a href="/student_details/${student.id}/" class="text-decoration-none">
                                                <div class="student-card">
                                                    <div class="student-info">
                                                        <img src="${student.photo || '/static/images/images.jpeg'}" 
                                                             alt="${student.surname}'s photo" 
                                                             class="student-image" />
                                                        <div class="student-details">
                                                            <h3>${student.surname} ${student.other_names}</h3>
                                                            <p>Matric Number: ${student.matric_number}</p>
                                                            <p>Level: ${student.level}L</p>
                                                            <p>Department: ${student.department}</p>
                                                        </div>
                                                    </div>
                                                    <input type="checkbox" class="student-checkbox" data-level="${student.level}" />
                                                </div>
                                            </a>
                                        `).join('')}
                                    </div>
                                `;
                                
                                searchResults.appendChild(levelSection);
                            }
                        });
                        
                        searchResults.style.display = 'block';
                    } else {
                        searchResults.innerHTML = `
                            <div class="no-results">
                                <p>No students found matching "${searchTerm}"</p>
                            </div>
                        `;
                        searchResults.style.display = 'block';
                    }
                });
        }, 300);
    });

    // Close search results when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchResults.contains(e.target) && e.target !== searchInput) {
            searchResults.style.display = 'none';
        }
    });

    // Handle Select All functionality
    const selectAllButtons = document.querySelectorAll('.select-all-btn');
    
    selectAllButtons.forEach(button => {
        button.addEventListener('click', function() {
            const level = this.getAttribute('data-level');
            const checkboxes = document.querySelectorAll(`.student-checkbox[data-level="${level}"]`);
            const isSelecting = this.textContent === 'SELECT ALL';
            
            checkboxes.forEach(checkbox => {
                checkbox.checked = isSelecting;
            });
            
            this.textContent = isSelecting ? 'DESELECT ALL' : 'SELECT ALL';
        });
    });

    // Handle individual checkbox clicks
    const checkboxes = document.querySelectorAll('.student-checkbox');
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('click', function(e) {
            e.stopPropagation();
            const level = this.getAttribute('data-level');
            const levelCheckboxes = document.querySelectorAll(`.student-checkbox[data-level="${level}"]`);
            const selectAllBtn = document.querySelector(`.select-all-btn[data-level="${level}"]`);
            const allChecked = Array.from(levelCheckboxes).every(cb => cb.checked);
            
            selectAllBtn.textContent = allChecked ? 'DESELECT ALL' : 'SELECT ALL';
        });
    });

    // Prevent checkbox clicks from triggering the card link
    document.querySelectorAll('.student-checkbox').forEach(checkbox => {
        checkbox.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            this.checked = !this.checked;
        });
    });
});

setTimeout(function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => alert.style.display = 'none');
}, 3000);

// Add event listener for staff search
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    let debounceTimer;

    if (searchInput) {
        searchInput.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            const searchTerm = this.value.trim();
            
            if (searchTerm.length < 2) {
                searchResults.style.display = 'none';
                return;
            }

            debounceTimer = setTimeout(() => {
                fetch(`/search_students/?term=${encodeURIComponent(searchTerm)}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.results.length) {
                            const studentsByLevel = {};
                            data.results.forEach(student => {
                                if (!studentsByLevel[student.level]) {
                                    studentsByLevel[student.level] = [];
                                }
                                studentsByLevel[student.level].push(student);
                            });

                            searchResults.innerHTML = '';
                            Object.keys(studentsByLevel).forEach(level => {
                                const levelSection = document.createElement('div');
                                levelSection.innerHTML = `
                                    <div class="search-level-header">Level ${level}</div>
                                    <div class="search-student-list">
                                        ${studentsByLevel[level].map(student => `
                                            <a href="/staff_student_details/${student.id}/" class="search-student-item">
                                                <img src="${student.photo || '/static/images/default.jpg'}" alt="${student.surname}'s photo" />
                                                <div>
                                                    <div class="student-name">${student.surname} ${student.other_names}</div>
                                                    <div class="student-info">
                                                        ${student.matric_number} - ${student.department}
                                                    </div>
                                                </div>
                                            </a>
                                        `).join('')}
                                    </div>
                                `;
                                searchResults.appendChild(levelSection);
                            });
                            searchResults.style.display = 'block';
                        } else {
                            searchResults.innerHTML = `
                                <div class="no-results">
                                    <p>No students found matching "${searchTerm}"</p>
                                </div>
                            `;
                            searchResults.style.display = 'block';
                        }
                    });
            }, 300);
        });
    }
});


