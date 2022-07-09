// ファイルサイズのバリデーション
const sizeLimit = 1024 * 500;
const fileInput = document.getElementById('image');
function img_check() {
    var file = fileInput.files[0];
    if (file.size > sizeLimit) {
        fileInput.setCustomValidity("size_error");
        return;
    }
    fileInput.setCustomValidity("");
}

// IDのバリデーション
const no_seven = document.getElementById('no_seven');
const no_family = document.getElementById('no_family');
function no_check($this) {
    $this.value = $this.value.toUpperCase();
    if ($this.value) {
        if ($this == no_seven) {
            no_family.removeAttribute('required');
        } else if ($this == no_family) {
            no_seven.removeAttribute('required');
        }
    } else {
        if ($this == no_seven) {
            no_family.setAttribute('required', 'required');
        } else if ($this == no_family) {
            no_seven.setAttribute('required', 'required');
        }
    }
}

// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            } else {
                if (!window.confirm('登録してよろしいですか？')) {
                    event.preventDefault()
                    event.stopPropagation()
                }
            }

            form.classList.add('was-validated')
        }, false)
    })
})()