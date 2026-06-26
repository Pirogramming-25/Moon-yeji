window.onload = function () {

    const pw_show_hide = document.querySelector('.pw_show_hide');
    const input_id = document.querySelector('input[type=text]');
    const input_pw = document.querySelector('input[type=password]');
    const id_error = document.querySelector('.id_error');
    const pw_error = document.querySelector('.pw_error');

    console.log(pw_show_hide, input_id, input_pw, id_error, pw_error);

    // 아이디 입력창 클릭 시 에러 표시
    input_id.addEventListener('click', function () {
        id_error.style.display = 'block';
    });

    // 비밀번호 입력창 클릭 시 에러 표시
    input_pw.addEventListener('click', function () {
        pw_error.style.display = 'block';
    });

    // 비밀번호 보기/숨기기 버튼
    let i = true;

    pw_show_hide.addEventListener('click', function () {

        if (i == true) {
            pw_show_hide.style.backgroundPosition = '-126px 0';
            input_pw.type = 'text';      // 비밀번호 보이기
            i = false;
        } else {
            pw_show_hide.style.backgroundPosition = '-105px 0';
            input_pw.type = 'password';  // 비밀번호 숨기기
            i = true;
        }

    });

} // onload end