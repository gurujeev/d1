/* =========================
   THEME
========================= */

function applyTheme(theme) {

    document.documentElement
        .setAttribute(
            "data-theme",
            theme
        );

    localStorage.setItem(
        "theme",
        theme
    );


    const icon =
        document.querySelector(
            "#themeToggle i"
        );

    if (!icon) return;


    if (theme === "dark") {

        icon.className =
            "bi bi-sun-fill";

    } else {

        icon.className =
            "bi bi-moon-stars-fill";
    }
}


function initializeTheme() {

    const savedTheme =
        localStorage.getItem("theme");


    if (savedTheme) {

        applyTheme(savedTheme);

        return;
    }


    const systemDark =
        window.matchMedia(
            "(prefers-color-scheme: dark)"
        ).matches;


    applyTheme(
        systemDark ? "dark" : "light"
    );
}


document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeTheme();


        const toggle =
            document.querySelector(
                "#themeToggle"
            );


        if (toggle) {

            toggle.addEventListener(
                "click",
                () => {

                    const current =
                        document.documentElement
                            .getAttribute(
                                "data-theme"
                            );


                    applyTheme(
                        current === "dark"
                            ? "light"
                            : "dark"
                    );
                }
            );
        }
    }
);


/* =========================
   PASSWORD
========================= */

function togglePassword(
    inputId,
    button
) {

    const input =
        document.getElementById(
            inputId
        );

    const icon =
        button.querySelector("i");


    if (input.type === "password") {

        input.type = "text";

        icon.className =
            "bi bi-eye-slash";

    } else {

        input.type = "password";

        icon.className =
            "bi bi-eye";
    }
}


/* =========================
   LOGIN
========================= */

const loginForm =
    document.getElementById(
        "loginForm"
    );


if (loginForm) {

    loginForm.addEventListener(
        "submit",
        async (event) => {

            event.preventDefault();


            const email =
                document.getElementById(
                    "email"
                ).value.trim();


            const password =
                document.getElementById(
                    "password"
                ).value;


            const message =
                document.getElementById(
                    "loginMessage"
                );


            const loginText =
                document.getElementById(
                    "loginText"
                );


            const spinner =
                document.getElementById(
                    "loginSpinner"
                );


            message.classList.add(
                "d-none"
            );


            loginText.textContent =
                "Signing in...";

            spinner.classList.remove(
                "d-none"
            );


            try {

                const data =
                    await apiRequest(
                        "/auth/login",
                        {
                            method: "POST",

                            body: JSON.stringify({
                                email,
                                password
                            })
                        }
                    );


                localStorage.setItem(
                    "access_token",
                    data.access_token
                );


                localStorage.setItem(
                    "user_role",
                    data.role
                );


                localStorage.setItem(
                    "user_name",
                    data.name
                );


                redirectByRole(
                    data.role
                );


            } catch (error) {

                message.textContent =
                    error.message;

                message.className =
                    "alert alert-danger";


            } finally {

                loginText.textContent =
                    "Sign in";

                spinner.classList.add(
                    "d-none"
                );
            }
        }
    );
}


/* =========================
   ROLE REDIRECT
========================= */

function redirectByRole(role) {

    switch (role) {

        case "student":

            window.location.href =
                "/student/dashboard.html";

            break;


        case "mentor":

            window.location.href =
                "/mentor/dashboard.html";

            break;


        case "coordinator":

            window.location.href =
                "/coordinator/dashboard.html";

            break;


        case "attendance_operator":

            window.location.href =
                "/attendance/dashboard.html";

            break;


        case "hod":

            window.location.href =
                "/hod/dashboard.html";

            break;


        default:

            alert(
                "Your account role is not configured."
            );
    }
}