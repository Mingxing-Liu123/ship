//var List={{List|safe}};
//检查发射节点与接收节点是否已经选择，如果没有选择，则不提交表单
function submit_sure()
{
    var send = document.getElementsByName("sendnode");
    var recv = document.getElementsByName("recvnode");
    var check1=-1;
    var check2=-1;
    for(var i=0;i<send.length;++i){
        console.log(send[i].checked);
        if(send[i].checked)
            check1 = i;
        if(recv[i].checked)
            check2 = i;
    }
    if(check1 == -1){
        alert("请选择发射节点");
        return false;
    }
    if(check2 == -1){
        alert("请选择接收节点");
        return false;
    }
    if(check1 == check2){
        alert("发射节点不能与接收节点一样")
        return false;
    }
    var sure = confirm("确定要提交么？")
    if(sure==true){
        return true; 
    }   
    else
        return false;
}

//在没有权限的时候，提交参数表
function no_access_submit()
{
    alert("提交失败！您还没登录，请您登录之后再提交")
}
// 硬件仿真界面
/****
 * 查看仿真节点
 * 
*/
function submit_see_node(){

    
}
/**
 * 提交仿真
 */
function submit_emulation(){

}
/*
提交评论
*/
function submit_comment(){
    var sure = confirm("确定要提交么？")
    if(sure==true){
        return true; 
    }   
    else
        return false;
}