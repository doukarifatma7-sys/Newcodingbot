// DOM Elements
const passwordField = document.getElementById('password');
const confirmPasswordField = document.getElementById('confirmPassword');
const togglePasswordBtn = document.getElementById('togglePassword');
const toggleConfirmPasswordBtn = document.getElementById('toggleConfirmPassword');
const passwordMatch = document.getElementById('passwordMatch');
const strengthText = document.getElementById('strengthText');
const strengthBars = [
    document.getElementById('strengthFill1'),
    document.getElementById('strengthFill2'),
    document.getElementById('strengthFill3'),
    document.getElementById('strengthFill4')
];
const successMessage = document.getElementById('successMessage');
const form = document.getElementById('signupForm');

function showError(input, message){
    const error = document.getElementById(input.id + 'Error');
    input.classList.add('input-error');
    error.textContent = message;
    error.style.display = 'block';
}

function clearError(input){
    const error = document.getElementById(input.id + 'Error');
    input.classList.remove('input-error');
    error.style.display = 'none';
}

function isValidEmail(email){
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function isValidPhone(phone){
    return /^[0-9]{10}$/.test(phone);
}

// Toggle password visibility
togglePasswordBtn.addEventListener('click', function() {
    const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordField.setAttribute('type', type);
    this.innerHTML = type === 'password' ? '<i class="far fa-eye"></i>' : '<i class="far fa-eye-slash"></i>';
});

toggleConfirmPasswordBtn.addEventListener('click', function() {
    const type = confirmPasswordField.getAttribute('type') === 'password' ? 'text' : 'password';
    confirmPasswordField.setAttribute('type', type);
    this.innerHTML = type === 'password' ? '<i class="far fa-eye"></i>' : '<i class="far fa-eye-slash"></i>';
});

// Password strength indicator
passwordField.addEventListener('input', function() {
    const password = this.value;
    let strength = 0;
    if(password.length >= 8) strength++;
    if(/[A-Z]/.test(password)) strength++;
    if(/[0-9]/.test(password)) strength++;
    if(/[^A-Za-z0-9]/.test(password)) strength++;

    strengthBars.forEach((bar, index) => {
        if(index < strength){
            bar.style.width = '100%';
            if(strength===1){bar.style.backgroundColor='#ff4757'; strengthText.textContent='Weak'; strengthText.style.color='#ff4757';}
            else if(strength===2){bar.style.backgroundColor='#ffa502'; strengthText.textContent='Fair'; strengthText.style.color='#ffa502';}
            else if(strength===3){bar.style.backgroundColor='#ffc107'; strengthText.textContent='Good'; strengthText.style.color='#ffc107';}
            else if(strength===4){bar.style.backgroundColor='#00c896'; strengthText.textContent='Strong'; strengthText.style.color='#00c896';}
        } else bar.style.width='0%';
    });

    checkPasswordMatch();
});

// Real-time password confirmation check
confirmPasswordField.addEventListener('input', checkPasswordMatch);

function checkPasswordMatch(){
    const password = passwordField.value;
    const confirmPassword = confirmPasswordField.value;

    if(confirmPassword.length === 0){
        passwordMatch.style.opacity='0';
        confirmPasswordField.style.borderColor='#e2e8f0';
    } else if(password === confirmPassword){
        passwordMatch.style.opacity='1';
        passwordMatch.className='password-match match-success';
        passwordMatch.innerHTML='<i class="fas fa-check-circle"></i><span>Passwords match</span>';
        confirmPasswordField.style.borderColor='#00c896';
    } else {
        passwordMatch.style.opacity='1';
        passwordMatch.className='password-match match-error';
        passwordMatch.innerHTML='<i class="fas fa-exclamation-circle"></i><span>Passwords do not match</span>';
        confirmPasswordField.style.borderColor='#ff4757';
    }
}

// Form submission
form.addEventListener('submit', function(e){
    e.preventDefault();
    let valid = true;

    const firstName = document.getElementById('firstName');
    const lastName = document.getElementById('lastName');
    const email = document.getElementById('email');
    const phone = document.getElementById('phone');
    const password = passwordField;
    const confirmPassword = confirmPasswordField;
    const terms = document.getElementById('terms');

    if(firstName.value.trim() === ''){ showError(firstName,'First name is required'); valid=false; } else clearError(firstName);
    if(lastName.value.trim() === ''){ showError(lastName,'Last name is required'); valid=false; } else clearError(lastName);
    if(!isValidEmail(email.value)){ showError(email,'Invalid email address'); valid=false; } else clearError(email);
    if(!isValidPhone(phone.value)){ showError(phone,'Phone must be 10 digits'); valid=false; } else clearError(phone);
    if(password.value.length<8){ showError(password,'Minimum 8 characters'); valid=false; } else clearError(password);
    if(password.value!==confirmPassword.value){ showError(confirmPassword,'Passwords do not match'); valid=false; } else clearError(confirmPassword);
    if(!terms.checked){ document.getElementById('termsError').style.display='block'; valid=false; } else document.getElementById('termsError').style.display='none';

    if(!valid) return;

    successMessage.querySelector('.success-text h3').textContent='Welcome to Smart Ride DZ!';
    successMessage.querySelector('.success-text p').textContent='Your journey to premium transportation begins now.';
    successMessage.classList.add('show');

    setTimeout(()=>{ successMessage.classList.remove('show'); }, 5000);

    console.log('Form submitted successfully');
});