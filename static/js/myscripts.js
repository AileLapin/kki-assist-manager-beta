window.onload = function(){
    var list = document.getElementsByClassName("trouble-content");
    for(var i=0, len=list.length; i<len; i++){
	var child = list[i].firstElementChild;
	var con = child.textContent;
	if(con.length > 45){
	    child.textContent = con.substr(0, 40)+". . .";
	    //document.getElementById("trouble_content_loader").classList.remove("display-none");
	    //document.getElementById("trouble_content_loader").classList.remove("display-none");
	}
	child.className = "";
    }
}

function trouble_page_scripts(){
    // ================== troubleアプリケーションのcolumn移動 ====================
    function move_column(col, _from, to){
	col.classList.remove(_from);
	col.classList.add(to);
	console.log("move!");
    }
    // ================== is-activeのtoggle ===================================
    function clear_active(list){
	for(var i=0, len=list.length; i<len; i++){
	    list.item(i).classList.remove("is-active");
	}
    }
    
    var troubles = document.getElementsByClassName("trouble-card");
    // ================== クリック時のcolumn移動のイベントリスナー登録 =============
    for(var i=0, len=troubles.length; i < len; i++){
	troubles.item(i).addEventListener("click", function(){
	    console.log(this.id);
	    
	    var xhr = new XMLHttpRequest();
	    xhr.onreadystatechange = function(){
		if (xhr.readyState === 4){ // 通信が完了した時
		    if (xhr.status === 200){ // 通信が成功した時
			var trouble = JSON.parse(xhr.responseText);
			if (trouble === null){ // troubleが存在しない場合
			    console.log("not found")
			} else { // troubleが存在したら書き換える
			    // detail-colmunの値を書き換える
			    if(trouble["permission"] === "True"){
				document.getElementById("permission").textContent = "True";
				document.getElementById("update_mark").classList.add("is-active");
				document.getElementById("delete_mark").classList.add("is-active");
			    }else{
				document.getElementById("permission").textContent = "False";
				document.getElementById("update_mark").classList.remove("is-active");
				document.getElementById("delete_mark").classList.remove("is-active");
			    }
			    var ary = Array("pk", "reporter", "carer", "occur_date",
					    "occur_machine", "trouble_user", "content",
					    "approach", "report_date");
			    for (var i=0, len=ary.length; i<len; i++){// aryをキーとして値を設定する
				document.getElementById(ary[i]).textContent = trouble[ary[i]];
			    }
			    document.getElementById("pk").dataset.pk = trouble["pk"];
			    document.getElementById("carer").dataset.carerPk = trouble["carer_pk"];
			    var date = document.getElementById("occur_date");
			    date.dataset.year = trouble["o_d_Y"];
			    date.dataset.mon = trouble["o_d_m"];
			    date.dataset.day = trouble["o_d_d"];
			    date.dataset.hour = trouble["o_d_H"];
			    date.dataset.min = trouble["o_d_M"];
			    date.dataset.sec = trouble["o_d_S"];
			    var machine = document.getElementById("occur_machine");
			    machine.dataset.type = trouble["o_m_type"];
			    machine.dataset.num = trouble["o_m_num"];
			    var t_user = document.getElementById("trouble_user");
			    t_user.dataset.year = trouble["t_u_year"];
			    t_user.dataset.num = trouble["t_u_num"];
			    //document.getElementById("trouble-detail-load").classList.add("display-none");
			    document.getElementById("trouble_detail_card_content").classList.remove("opa0");
			}
		    } else { // 通信が失敗した時
			console.log("failed")
		    }
		} else { // 通信が完了する前
		    console.log("wait...")
		    //document.getElementById("trouble-detail-load").classList.remove("display-none");
		    document.getElementById("trouble_detail_card_content").classList.add("opa0");
		}
	    };
	    //xhr.open("GET", "trouble/ajax/troubledetail?pk=" + encodeURIComponent(this.id));
	    xhr.open("GET", "trouble/ajax/troubledetail?pk=" + this.id);
	    xhr.send();
	    clear_active(troubles);
	    this.classList.add("is-active");
	    if(window.innerWidth < 960){
		move_column(document.getElementById("trouble_list"), "is-center", "is-left");
		move_column(document.getElementById("trouble_detail"), "is-right", "is-center");
		document.getElementById("hamburger-menu").style.display = "none";
		document.getElementById("back").style.display = "block";
	    }
	}, false)
    }

    document.getElementById("back").addEventListener("click", function(){
	console.log("click back!")
	clear_active(troubles)
	if(window.innerWidth < 960){
	    move_column(document.getElementById("trouble_list"), "is-left", "is-center");
	    move_column(document.getElementById("trouble_detail"), "is-center", "is-right");
	    document.getElementById("hamburger-menu").style.display = "block";
	    document.getElementById("back").style.display = "none";
	}
    }, false);

    // ==============================================
    // ========== trouble update ====================
    // permissionがTrueなら，update,delete_makrクリック時にformを出現させる
    document.getElementById("update_mark").addEventListener("click", function(){
	var permission = document.getElementById("permission").textContent;
	if(permission === "True"){
	    document.getElementById("update_form_input").checked = true;
	    var pk = document.getElementById("pk").dataset.pk;
	    var url = "/trouble/update/" + pk;
	    var form = document.forms.update_form;
	    form.action = url
	    form.carer.value = document.getElementById("carer").dataset.carerPk;
	    var date = document.getElementById("occur_date");
	    form.year.value = date.dataset.year;
	    form.month.value = date.dataset.mon;
	    form.day.value = date.dataset.day;
	    form.hour.value = date.dataset.hour;
	    form.minute.value = date.dataset.min;
	    var machine = document.getElementById("occur_machine");
	    form.occur_machine_type.value = machine.dataset.type;
	    form.occur_machine_num.value = machine.dataset.num;
	    var t_user = document.getElementById("trouble_user");
	    form.trouble_user_year.value = t_user.dataset.year;
	    form.trouble_user_num.value = t_user.dataset.num;
	    form.content.value = document.getElementById("content").textContent;
	    form.approach.value = document.getElementById("approach").textContent;
	}else{
	    console.log("False!");
	}
    }, false);
    // trouble delete form
    document.getElementById("delete_mark").addEventListener("click", function(){
	var permission = document.getElementById("permission").textContent;

	if(permission === "True"){
	    // 必要なデータを取り出しておく
	    var pk = document.getElementById("pk").textContent;
	    var url = "/trouble/delete/" + pk;
	    var form = document.forms.delete_form;
	    // formのアクションをセット
	    form.action = url

	    // forで回せるようにaryに名前を格納しておく．
	    var ary = Array("reporter", "carer", "occur_date",
			    "occur_machine", "trouble_user");
	    var td_list = document.querySelectorAll("#trouble_delete_form td");
	    var p_list = document.querySelectorAll("#trouble_delete_form section p");

	    for(var i=0, len=td_list.length; i<len; i++){
		td_list[i].textContent = document.getElementById(ary[i]).textContent;
	    }
	    
	    p_list[0].textContent = document.getElementById("content").textContent;
	    p_list[1].textContent = document.getElementById("approach").textContent;
	    document.getElementById("delete_form_input").checked = true;
	    console.log(document.getElementById("delete_form_input").checked);
	}else{
	    console.log("False!");
	}

    }, false);    
}

document.addEventListener("DOMContentLoaded", function(){
    document.getElementById("hamburger-menu").addEventListener("click", function(){
	document.getElementById("nav-input").checked = true;
    }, false);

    var pathname = location.pathname;
    if (pathname === "/trouble/"){
	trouble_page_scripts();
	console.log("!");
    }

    
}, false);
