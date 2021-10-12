$(document).ready(function () {

    $(document).on("click", ".country-btn", function () {
        click_button($(this), 'country')
    })

    $(document).on("click", ".nir-main-btn", function () {
        click_button($(this), '')
    })

    function click_button(par, flag) {
        var index = par.bind()[0]['id']
        var pk = document.getElementById('pk')
        if (flag === 'country') {
            index = index.slice(7);
            pk = document.getElementById('country')
        }
        if (pk !== null) {
            pk.value = index * 1
        }

        set_value_date('d_start', 'id_date_start')
        set_value_date('d_end', 'id_date_end')
    }

    function set_value_date(name_class, name_id) {
        let my_par = document.getElementById(name_id).value
        let name_par = document.getElementsByClassName(name_class)
        for (var i = 0; i < name_par.length; i++) {
            name_par[i].value = my_par
        }
    }


    var $myForm
    var $thisURL
    var $formData
    // форма создания комнаты модальное окно
    $(document).on("click", ".but-ajax-1", function () {
        $myForm = $('.form-ajax-1')
        actForm($myForm);
    })
    $(document).on("click", ".but-ajax-2", function () {
        $myForm = $('.form-ajax-2')
        actForm($myForm);
    })


    function actForm($myForm) {
        $myForm.addClass('form')
        $myForm.submit(function (event) {
            event.preventDefault();

            $formData = new FormData($(this).get(0)); // создаем новый экземпляр объекта и передаем ему нашу форму (*)
            //Обратите внимание на то, что передаем форму не объектом jQuery, а DOM-элемент,
            // чтобы передать картинку-файл
            $thisURL = $myForm.attr('data-url') || window.location.href // or set your own url
            postFunc($formData, $thisURL);
        })
    }

    function postFunc($formData, $thisURL) {
        $.ajax({
            method: "POST",
            url: $thisURL,
            data: $formData,
            contentType: false, // важно - убираем форматирование данных по умолчанию
            processData: false,// важно - убираем преобразование строк по умолчанию
            success: handleFormSuccess,
            error: handleFormError,
        })
    }

    function handleFormSuccess(data, textStatus, jqXHR) {

        var myMessDiv = document.getElementById('my-message')
        myMessDiv.style = "display:block";

        var myAlert = document.getElementById('mess-alert')
        myAlert.className = 'alert alert-dismissible fade show alert-success'

        var myMess = document.getElementById('my-mess')
        myMess.innerHTML = data['message'];
        $myForm[0].reset(); // reset form data
    }

    function handleFormError(jqXHR, textStatus, errorThrown) {

        var myMessDiv = document.getElementById('my-message')
        myMessDiv.style = "display:block";

        var myAlert = document.getElementById('mess-alert')
        myAlert.className = 'alert alert-dismissible fade show alert-danger'

        var myMess = document.getElementById('my-mess')
        myMess.innerHTML = textStatus + ': ' + errorThrown;
    }

    ///////////////////////////////////////////////////////////////////////////////////////////
    // установить 'checked' в параметр Категория или Сервис, заданный в GET-запросе
    //получить список параметров из GET-запроса
    // в виде списка:
    // ["country=", "date_start=", "date_end=", "min_price=", "max_price=", "category=5", "category=4", "service=1", "service=2"]
    var list_get_params = location.search.substring(1, location.search.length).split('&')
    // словарь входных параметров в виде
    //country: "4", date_start: "", date_end: ""
    var dict_pars = {}

    for (var j = 0; j < list_get_params.length; j += 1) {
        var s2 = list_get_params[j].split('=');
        if (s2[0] === 'service') {
            var k = s2[1] * 1 - 1
            set_attribute('service', k, "id_service_")
        }
        if (s2[0] === 'category') {
            var n = (s2[1] - 5) * (-1)
            set_attribute('category', n, "id_category_")
        }
        dict_pars[decodeURIComponent(s2[0]).toLowerCase()] = decodeURIComponent(s2[1]);
    }

    function set_attribute(name_par, k, name_id) {
        var ckk = document.getElementById(name_id + k)
        ckk.setAttribute('checked', 'checked')
    }
    ///////////////////////////////////////////////////////////////////////////////////////////


    ///////////////////////////////////////////////////////////////////////////////////////////
    // нарисовать ЗВЕЗДОЧКИ в Категория (тег ul)
    var bl_category = null
    bl_category = document.getElementById("id_category")
    if (bl_category !== null)  {
        if (bl_category.children.length > 0) {
            if (bl_category.children[0].nodeName !== 'LI') {
                bl_category = null
            }
        } else {
            bl_category = null
        }
    }
    if (bl_category !== null) {
        var mas = []
        var i = 5
        for (let elem of bl_category.children) {
            let child_label = elem.children.item(0) //это элемент label

            mas[i] = document.createElement('label')
            Object.assign(mas[i], child_label)
            let bl_5 = document.createElement('span')
            bl_5.className = "star-rating"
            let bl_s = []
            for (var g = 0; g < i; g++) {
                bl_s[g] = document.createElement('span')
                bl_s[g].className = "bi bi-star-fill"
                bl_s[g].setAttribute('style', 'padding-right:2px; padding-left:1.5px')
                bl_5.append(bl_s[g])
            }
            mas[i].append(bl_5)
            elem.children.item(0).append(mas[i])
            i--
        }
    } //(bl_category !== null
})



