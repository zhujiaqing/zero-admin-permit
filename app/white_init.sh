#!/bin/bash

redisCmd="redis-cli -h ops.redis.youja.cn -p 6610 -n 15 "

# member's admin
$redisCmd HMSET H:phonenumber 15900725153 jesse 18501799688 jesse 
$redisCmd HSET H:phonenumber 18007220799 anson 
$redisCmd HMSET H:phonenumber 13402067030 钱承霖 15000040466 姜文清 18516524022 施家豪 13675834713 张克诚 15000827154 朱佳伟 18016041993 朱家贤 18616275663 陈康
$redisCmd HMSET H:phonenumber 18321482567 张宁 18916176519 杨新 15198260184 陈果 17091838911 刘青 13122029801 李银 18016385713 杜明钊 18658883313 黄秒
$redisCmd HMSET H:phonenumber 13636597595 陈路 13651861065 朱家清 13601696170 杜德佑 18621784057 叶承阳 13818252513 孙长浩 13482216820 秦冰 15001738597 高伟
$redisCmd HMSET H:phonenumber 18601679678 王政 18621360995 frank 18018695552 camel

# domain's admin
$redisCmd HMSET H:admin:yw.admin.youja.cn author jesse backend '10.10.10.12:10002,10.10.10.61:10002' memo '运维工具接口'
$redisCmd HMSET H:admin:svn.youja.cn author jesse
$redisCmd HMSET H:admin:redmine.youja.cn author jesse
$redisCmd HMSET H:admin:gitlab.youja.cn author jesse
$redisCmd HMSET H:admin:mvn.repo.youja.cn author jesse
$redisCmd HMSET H:admin:uplus.admin.youja.cn author 待定
$redisCmd HMSET H:admin:statis.admin.youja.cn author 待定
$redisCmd HMSET H:admin:moplus.admin.youja.cn author 待定
$redisCmd HMSET H:admin:shentu.admin.youja.cn author 陈路
$redisCmd HMSET H:admin:rank.admin.youja.cn author 叶承阳
$redisCmd HMSET H:admin:topic.admin.youja.cn author 陈果
$redisCmd HMSET H:admin:pfact.admin.youja.cn author '李银'
$redisCmd HMSET H:admin:live.admin.youja.cn author '刘青,李银'
$redisCmd HMSET H:admin:show.admin.youja.cn author 陈果
$redisCmd HMSET H:admin:star.show.admin.youja.cn author 陈果




