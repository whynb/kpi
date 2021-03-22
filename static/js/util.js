/**
 * Created by why on 10/18/17.
 */

function tap(x){ console.log(x); return x; }

function getLastDayOfMonth(m) {
    var lastDay= new Date(m.substring(0, 4), m.substring(5,7), 0);
    var year = lastDay.getFullYear();
    var month = lastDay.getMonth() + 1;
    month = month < 10 ? '0'+ month : month;
    var day = lastDay.getDate();
    day = day < 10 ? '0'+day : day;
    return year + '-' + month + '-' + day;
}

function array_to_string(array) {
    var s = "('',";
    console.log(array);
    for (var i=0; i < array.length; i++) s += array[i]+',';
    return s.substr(0, s.length-1)+')';
}

function notValidIndex(val)
{
    var reg = /(^[0-9][0-9]([-|—][0-9][0-9])?([,|，][0-9][0-9]([-|—][0-9][0-9])?)*$)/;
    return !reg.test(val);
}

function notNumber(val) {
    // var reg = /(^[1-9][0-9]*$)|(^[1-9][0-9]*.[0-9]+$)|(^[0]$)|(^[0].[0-9]+$)/;
    var reg = /(^[1-9|\-1-9][0-9]*$)/;
    return !reg.test(val);
}

function notFloat(val) {
    var reg = /(^[1-9|\-1-9][0-9]*$)|(^[1-9|\-1-9][0-9]*.[0-9]{1,3}$)|(^[0]$)|(^[0|\-0].[0-9]{1,3}$)/;
    // var reg = /(^[1-9][0-9]*$)/;
    return !reg.test(val);
}

function notICCard(val) {
    var reg = /(^[0-9]{15,15}$)/;
    return !reg.test(val);
}

function checkTel(tel) {
    var mobile = /^1[3|5|6|7|8]\d{9}$/ , phone = /^0\d{2,3}-?\d{7,8}$/;
    return mobile.test(tel) || phone.test(tel);
}

// FROM blaster.html
function createElement(type, name) {
    var element = null;
    if (!element) {
        element = document.createElement(type);
        element.name = name;
    }
    return element;
}

function createRadioElement(parent, name, value, checked, text) {
    var e = document.createElement("input");
    e.name = name;
    e.type = "radio";
    e.value = value;

    if (checked == 'checked') {
        e.setAttribute("checked", checked);
    }

    var l = document.createElement("label");
    l.className = "radio-inline";
    l.appendChild(e);
    l.appendChild(document.createTextNode(text));

    parent.appendChild(l);
}

function getCookie(name)
{
    var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
    if(arr=document.cookie.match(reg)) {
        return decodeURI(arr[2]);
    }
    else
        return null;
}

function uuid() {
    var s = [];
    var hexDigits = "0123456789abcdef";
    for (var i = 0; i < 32; i++) {
        s[i] = hexDigits.substr(Math.floor(Math.random() * 0x10), 1);
    }
    s[12] = "4"; // bits 12-15 of the time_hi_and_version field to 0010
    s[16] = hexDigits.substr((s[16] & 0x3) | 0x8, 1); // bits 6-7 of the clock_seq_hi_and_reserved to 01
    // s[8] = s[13] = s[18] = s[23] = "-";

    var uuid = s.join("");
    return uuid;
}


function getDateString(AddDayCount = 0) {
    var dd = new Date();
    dd.setDate(dd.getDate() + AddDayCount); //获取AddDayCount天后的日期
    var y = dd.getFullYear();
    var m = dd.getMonth()+1; //获取当前月份的日期
    m = m.toString();
    if (m.length == 1){
        m = '0' + m
    }
    var d = dd.getDate();
    d = d.toString();
    if (d.length == 1){
        d = '0' + d
    }
    return y+"-"+m+"-"+d;
}

function getHourMinute() {
    var date = new Date();
    return '' + date.getHours() + '' + date.getMinutes();
}

function getHMS() {
    var date = new Date();
    return '' + date.getHours() + '' + date.getMinutes() + '' + date.getSeconds();
}

function getMonthString(AddDayCount) {
    return getDateString(AddDayCount).substring(0, 7);
}

// fow password management
function changepwd_onclick() { $('#passwordModal').modal(); }

function chineseSort(a, b) { return a.localeCompare(b); }

function pwd_onclick() {
    if (checkPwd()) {
        $.get("../changepwd?oldpwd="+oldpwd.value+"&newpwd="+newpwd.value, function(ret){
            $.hulla.send(ret['tag'], "info");
            if (ret['success']){
                $('#passwordModal').modal('hide');
                $('#passwordModal').removeData("bs.modal");
            }
        });
    }
}

function checkPwd() {
    if ($('#oldpwd').val() == "") { $.hulla.send("原密码不能为空", "danger"); return false; }
    if ($('#newpwd').val() == "") { $.hulla.send("新密码不能为空", "danger"); return false; }
    if ($('#conpwd').val() == "") { $.hulla.send("确认密码不能为空", "danger"); return false; }
    if ($('#newpwd').val() != $('#conpwd').val()) { $.hulla.send("两次新密码不一致，请重新输入", "danger"); return false; }
    if ($('#newpwd').val() == $('#oldpwd').val()) { $.hulla.send("新旧密码相同，请重新输入", "danger"); return false; }
    return true;
}

function selectpickerByTable(table, col_name, select, include_all) {
    include_all = include_all||false;
    $.getJSON("../get_table?table="+table, function(ret){
        $(select).html('');
        if (include_all) { $("<option value=\"-1\">全部</option>").appendTo($(select)); }
        for(var i=0; i < ret.length; i++){
            $("<option value="+ret[i].id+">"+ret[i][col_name]+"</option>").appendTo($(select));
        }
        $(select).selectpicker('refresh');
    });
}

function valid_month(s) {
    var str = s + "-01";
    var r = str.match(/^(\d{4})(-|\/)(\d{2})\2(\d{2})$/);
    if (r == null) return false;
    var d = new Date(r[1], r[3]-1, r[4]);
    return (d.getFullYear() == r[1] && (d.getMonth()+1) == r[3] && d.getDate() == r[4]);
}

function valid_date(str) {
    var r = str.match(/^(\d{4})(-|\/)(\d{2})\2(\d{2})$/);
    if (r == null) return false;
    var d = new Date(r[1], r[3]-1, r[4]);
    return (d.getFullYear() == r[1] && (d.getMonth()+1) == r[3] && d.getDate() == r[4]);
}

function randomString(length) {
    var chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    chars = '0123456789abcdefghijklmnopqrstuvwxyz';
    var result = '';
    for (var i = length; i > 0; --i) result += chars[Math.floor(Math.random() * chars.length)];
    return result;
}

function randomDigital(length) {
    var chars = '0123456789';
    var result = '1';
    for (var i = length-1; i > 0; --i) result += chars[Math.floor(Math.random() * chars.length)];
    return result;
}

function chineseSort(a, b){
    return a.localeCompare(b);
}


// 判断是否含有class
function hasClass(el, className) {
  let reg = new RegExp('(^|\\s)' + className + '(\\s|$)')
  return reg.test(el.className)
}

// el元素添加某个class
function addClass(el, className) {
  if (hasClass(el, className)) {
    return
  }
  let newClass = el.className.split(' ')
  newClass.push(className)
  el.className = newClass.join(' ')
}

// 移除el元素某个class
function removeClass(el, className) {
  if (!hasClass(el, className)) {
    return
  }
  let reg = new RegExp('(^|\\s)' + className + '(\\s|$)', 'g')
  el.className = el.className.replace(reg, ' ')
}

// 数组去重
function arrayRemoval(arr) {
  // 方法一
  return [...new Set(arr)]
  // 方法二
  var obj = {};
  return arr.filter(ele => {
    if (!obj[ele]) {
      obj[ele] = true;
      return true;
    }
  })
  // 方法三
  var result = [];
  arr.forEach(ele => {
    if (result.indexOf(ele) == -1) {
      result.push(ele)
    }
  })
  return result;
}

// 获取当前日期和时间
function getDateTime() {
  var date = new Date(),
    year = date.getFullYear(),
    month = date.getMonth() + 1,
    day = date.getDate(),
    hour = date.getHours() + 1,
    minute = date.getMinutes(),
    second = date.getSeconds();
  month = addZero(month);
  day = addZero(day);
  hour = addZero(hour);
  minute = addZero(minute);
  second = addZero(second);
  
  function addZero(i) {
    if (i < 10) {
      i = "0" + i;
    }
    return i;
  }
  return "" + year + "年" + month + "月" + day + "日" + hour + "时" + minute + "分" + second + "秒"
}

// 获取浏览器窗口宽高
function getViewportOffset() {
  if (window.innerWidth) {
    return {
      w: window.innerWidth,
      h: window.innerHeight
    }
  } else {
    if (document.compatMode === "BackCompat") {
      return {
        w: document.body.clientWidth,
        h: document.body.clientHeight
      }
    } else {
      return {
        w: document.documentElement.clientWidth,
        h: document.documentElement.clientHeight
      }
    }
  }
}

// 获取地址栏参数
function getHrefParams() {
  var sHref = window.location.href;
  var args = sHref.split('?');
  if (args[0] === sHref) {
    return '';
  }
  var hrefarr = args[1].split('#')[0].split('&');
  var obj = {};
  for (var i = 0; i < hrefarr.length; i++) {
    hrefarr[i] = hrefarr[i].split('=');
    obj[hrefarr[i][0]] = hrefarr[i][1];
  }
  return obj;
}

// 数组排序
function sortArr(arr) {
  // 方法一
  if (arr.length <= 1) {
    return arr;
  }
  var left = [],
    right = [];
  var pIndex = Math.floor(arr.length / 2);
  var p = arr.splice(pIndex, 1)[0];
  for (var i = 0; i < arr.length; i++) {
    if (arr[i] <= p) {
      left.push(arr[i]);
    } else {
      right.push(arr[i]);
    }
  }
  return sortArr(left).concat([p], sortArr(right));
  
  // 方法二
  for (var i = 0; i < arr.length - 1; i++) {
    for (var j = i + 1; j < arr.length; j++) {
      if (arr[i] > arr[j]) {
        var temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
      }
    }
  }
  return arr;
}

// 异步加载script脚本
function asyncLoadScript(src) {
  const s = document.createElement('script');
  s.type = 'text/JavaScript';
  s.async = true;
  s.src = src;
  const t = document.getElementsByTagName('script')[0];
  t.parentNode.insertBefore(s, t);
}

// 回到顶部
function scrollToTop() {
  const c = document.documentElement.scrollTop || document.body.scrollTop;
  if (c > 0) {
    window.requestAnimationFrame(scrollToTop);
    window.scrollTo(0, c - c / 8);
  }
}
