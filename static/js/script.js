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
});


  setTimeout(function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => alert.style.display = 'none');
  }, 3000);


