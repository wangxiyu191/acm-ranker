var casper = require('casper').create( {verbose: true});
var utils = require('utils');
var cid = casper.cli.args[0];
var password = casper.cli.args[1];
casper.start('http://acm.hust.edu.cn/vjudge/contest/view.action?cid=' + cid.toString() + '#rank');
casper.then(function () {
    //this.echo(this.getTitle(), 'INFO');
    this.evaluate(function (password) {
        document.querySelector("#contest_password").value = password;
    },{password:password})
    this.click("body > div:nth-child(11) > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button:nth-child(1)");
});
casper.then(function () {
    casper.wait(1000, function () {
        //this.echo("Login!", 'INFO');
    });
});
casper.then(function () {
    this.evaluate(function () {
        Vjudge.storage.set("show_animation", false);//关闭动画
        Vjudge.storage.set("show_nick", false);//不显示昵称
        Vjudge.storage.set("show_username", true);//显示用户名
        Vjudge.storage.set("include_practice", false);//不包括结束后提交的
        Vjudge.storage.set("show_all_teams", true);//显示所有队伍
    })
    this.click("#rank_setting");//打开rank设置
    casper.wait(1000, function () {
        //等加载
    });
});
casper.then(function () {
    this.click("body > div:nth-child(15) > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button");
});
casper.then(function () {
    //this.echo("format rank",'INFO');
    ranks= this.evaluate(getRanks);
    info={
        name:this.getTitle(),
        ranks:ranks
    }
    console.log(JSON.stringify(info));
});

function getRanks() {
    var links = document.querySelectorAll('#rank_data_source > div');
    var result=new Array();
    for(var i=0;i<=70;i++){
        if(links[i+1].childNodes[0].innerText===undefined){
            break;
        }
        result[i]=new Array();
        for(var j=0;j<4;j++){//取前4列
            result[i][j]=links[i+1].childNodes[j].innerText;
        }
    }
    return result;

}

casper.run();