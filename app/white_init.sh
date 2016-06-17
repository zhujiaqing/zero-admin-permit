#!/bin/bash

redisCmd="redis-cli -h ops.redis.youja.cn -p 6610 -n 15 "

# member's admin
$redisCmd HMSET H:phonenumber 15900725153 jesse 18501799688 jesse 
$redisCmd HSET H:phonenumber 18007220799 anson 
$redisCmd HSET H:phonenumber 13402067030 钱承霖 
$redisCmd HSET H:phonenumber 15000040466 姜文清
$redisCmd HSET H:phonenumber 18516524022 施家豪
$redisCmd HSET H:phonenumber 13675834713 张克诚
$redisCmd HSET H:phonenumber 15000827154 朱佳伟
$redisCmd HSET H:phonenumber 18016041993 朱家贤
$redisCmd HSET H:phonenumber 18616275663 陈康

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




