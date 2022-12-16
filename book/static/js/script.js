$(document).ready(function () {
	$(document).on("click", ".dropdown-menu", function (e) {
		e.stopPropagation();
	});

	$(".js-check :radio").change(function () {
		var check_attr_name = $(this).attr("name");
		if ($(this).is(":checked")) {
			$("input[name=" + check_attr_name + "]")
				.closest(".js-check")
				.removeClass("active");
			$(this).closest(".js-check").addClass("active");
			// item.find('.radio').find('span').text('Add');
		} else {
			item.removeClass("active");
			// item.find('.radio').find('span').text('Unselect');
		}
	});

	$(".js-check :checkbox").change(function () {
		var check_attr_name = $(this).attr("name");
		if ($(this).is(":checked")) {
			$(this).closest(".js-check").addClass("active");
			// item.find('.radio').find('span').text('Add');
		} else {
			$(this).closest(".js-check").removeClass("active");
			// item.find('.radio').find('span').text('Unselect');
		}
	});

	//////////////////////// Bootstrap tooltip
	if ($('[data-toggle="tooltip"]').length > 0) {
		// check if element exists
		$('[data-toggle="tooltip"]').tooltip();
	} // end if

	// custom
	for (let i = 2; i <= 4; i++) {
		$(`.check${i}`).click(function () {
			$(`#checkAll${i}`).removeAttr('checked');
		});
		$(`#checkAll${i}`).click(function () {
			const listCheck = document.querySelectorAll(`.check${i}`);
			listCheck.forEach(function (element, i) {
				element.checked = true
			})
		})
	}

	//sort
	$('.sort').click(function (e) {
		e.preventDefault();
		let url = new URLSearchParams(window.location.search);
		var hrefValue = this.href.slice(-3)
		url.set('sort', hrefValue);
		window.location.search = url;
	});

	$("#myBtn").click(function () {
		$('.toast').toast('show')
	});;

	const host = "https://provinces.open-api.vn/api/";
	var callAPI = (api) => {
		return axios.get(api)
			.then((response) => {
				renderData(response.data, "province");
			});
	}
	callAPI('https://provinces.open-api.vn/api/?depth=1');
	var callApiDistrict = (api) => {
		return axios.get(api)
			.then((response) => {
				renderData(response.data.districts, "district");
			});
	}
	var callApiWard = (api) => {
		return axios.get(api)
			.then((response) => {
				renderData(response.data.wards, "ward");
			});
	}

	var renderData = (array, select) => {
		let row = ' <option disable value="">Vui lòng chọn</option>';
		array.forEach(element => {
			row += `<option value="${element.code}">${element.name}</option>`
		});
		document.querySelector("#" + select).innerHTML = row
	}

	$("#province").change(() => {
		callApiDistrict(host + "p/" + $("#province").val() + "?depth=2");
		printResult();
	});
	$("#district").change(() => {
		callApiWard(host + "d/" + $("#district").val() + "?depth=2");
		printResult();
	});
	$("#ward").change(() => {
		printResult();
	})

	var printResult = () => {
		if ($("#district").val() != "" && $("#province").val() != "" &&
			$("#ward").val() != "") {
			let result = $("#ward option:selected").text() +
				" - " + $("#district option:selected").text() + " - " +
				$("#province option:selected").text();
			document.getElementById("result").value = result;
		}

	}
});

setTimeout(() => {
	$("#alert-messages").fadeOut("slow");
}, 4000);

function validateNumberPhone() {
	var phone = document.getElementById("phone_order").value;
	const regexPhoneNumber = /(84|0[3|5|7|8|9])+([0-9]{8})\b/g;
	let check = phone.match(regexPhoneNumber) ? true : false
	if (check == false) {
		alert("Số điện thoại không chính xác")
		return false;
	}
	return true;
}

function validationRegister() {
	var phone = document.getElementById("phone").value;
	var email = document.getElementById("email").value;
	var password1 = document.getElementById("password1").value;
	var password2 = document.getElementById("password2").value;

	let regex = new RegExp('[a-z0-9]+@[a-z]+\.[a-z]{2,3}');
	if (!email.match(regex)) {
		alert("Email không đúng định dạng");
		return false;
	}

	const regexPhoneNumber = /(84|0[3|5|7|8|9])+([0-9]{8})\b/g;
	let check = phone.match(regexPhoneNumber) ? true : false
	if (check == false || phone.length != 10) {
		alert("Số điện thoại không chính xác")
		return false;
	}
	if (password1.length < 8) {
		alert("Mật khẩu ít nhất 8 ký tự!")
		return false;
	}
	if (password1 != password2) {
		alert("Mật khẩu không trùng khớp!");
		return false;
	}
	return true;

};
