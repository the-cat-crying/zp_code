# -*- coding:utf-8 -*-

# ************************************************* os.access() ************************************************
"""
os.access() 方法使用当前的uid/gid尝试访问路径。大部分操作使用有效的 uid/gid, 因此运行环境可以在 suid/sgid 环境尝试。
access()方法语法格式如下：
    os.access(path, mode);
        path -- 要用来检测是否有访问权限的路径。
        mode -- mode为F_OK，测试存在的路径，或者它可以是包含R_OK, W_OK和X_OK或者R_OK, W_OK和X_OK其中之一或者更多。
        os.F_OK: 作为access()的mode参数，测试path是否存在。
        os.R_OK: 包含在access()的mode参数中 ， 测试path是否可读。
        os.W_OK 包含在access()的mode参数中 ， 测试path是否可写。
        os.X_OK 包含在access()的mode参数中 ，测试path是否可执行。
返回值
如果允许访问返回 True , 否则返回False。

ret = os.access("/tmp/foo.txt", os.F_OK)
print ("F_OK - 返回值 %s"% ret)
F_OK - 返回值 True
"""
# ************************************************* os.chdir() *************************************************
"""
os.chdir() 方法用于改变当前工作目录到指定的路径。
chdir()方法语法格式如下：
    os.chdir(path)
        path -- 要切换到的新路径。
返回值
如果允许访问返回 True , 否则返回False。
path = "/tmp"

# 查看当前工作目录
retval = os.getcwd()
print ("当前工作目录为 %s" % retval)
# 修改当前工作目录
os.chdir( path )
# 查看修改后的工作目录
retval = os.getcwd()
"""
# ************************************************* os.chflags() ***********************************************
"""
os.chflags() 方法用于设置路径的标记为数字标记。多个标记可以使用 OR 来组合起来。
只支持在 Unix 下使用。
chflags()方法语法格式如下：
    os.chflags(path, flags)
        path -- 文件名路径或目录路径。
        flags -- 可以是以下值：
            stat.UF_NODUMP: 非转储文件
            stat.UF_IMMUTABLE: 文件是只读的
            stat.UF_APPEND: 文件只能追加内容
            stat.UF_NOUNLINK: 文件不可删除
            stat.UF_OPAQUE: 目录不透明，需要通过联合堆栈查看
            stat.SF_ARCHIVED: 可存档文件(超级用户可设)
            stat.SF_IMMUTABLE: 文件是只读的(超级用户可设)
            stat.SF_APPEND: 文件只能追加内容(超级用户可设)
            stat.SF_NOUNLINK: 文件不可删除(超级用户可设)
            stat.SF_SNAPSHOT: 快照文件(超级用户可设)
该方法没有返回值。
path = "/tmp/foo.txt"
# 为文件设置标记，使得它不能被重命名和删除
flags = stat.SF_NOUNLINK
retval = os.chflags( path, flags )
print ("返回值: %s" % retval)
返回值: None
"""
# ************************************************* os.chmod() *************************************************
"""
os.chmod() 方法用于更改文件或目录的权限。
Unix 系统可用。
chmod()方法语法格式如下：
    os.chmod(path, mode)
        path -- 文件名路径或目录路径。
        flags -- 可用以下选项按位或操作生成，目录的读权限表示可以获取目录里文件名列表，执行权限表示可以把工作目录切换到此目录，
        删除添加目录里的文件必须同时有写和执行权限，文件权限以用户id->组id->其它顺序检验,最先匹配的允许或禁止权限被应用。
            stat.S_IXOTH: 其他用户有执行权0o001
            stat.S_IWOTH: 其他用户有写权限0o002
            stat.S_IROTH: 其他用户有读权限0o004
            stat.S_IRWXO: 其他用户有全部权限(权限掩码)0o007
            stat.S_IXGRP: 组用户有执行权限0o010
            stat.S_IWGRP: 组用户有写权限0o020
            stat.S_IRGRP: 组用户有读权限0o040
            stat.S_IRWXG: 组用户有全部权限(权限掩码)0o070
            stat.S_IXUSR: 拥有者具有执行权限0o100
            stat.S_IWUSR: 拥有者具有写权限0o200
            stat.S_IRUSR: 拥有者具有读权限0o400
            stat.S_IRWXU: 拥有者有全部权限(权限掩码)0o700
            stat.S_ISVTX: 目录里文件目录只有拥有者才可删除更改0o1000
            stat.S_ISGID: 执行此文件其进程有效组为文件所在组0o2000
            stat.S_ISUID: 执行此文件其进程有效用户为文件所有者0o4000
            stat.S_IREAD: windows下设为只读
            stat.S_IWRITE: windows下取消只读
"""
# ************************************************* os.getcwd() ************************************************
"""
os.getcwd() 方法用于返回当前工作目录。
    getcwd()方法语法格式如下：
        os.getcwd()
"""
# ************************************************* os.link() **************************************************
"""
os.link() 方法用于创建硬链接，名为参数 dst，指向参数 src。
该方法对于创建一个已存在文件的拷贝是非常有用的。
只支持在 Unix, Windows 下使用。
link()方法语法格式如下：
    os.link(src, dst)
        src -- 用于创建硬连接的源地址
        dst -- 用于创建硬连接的目标地址
        
path = "/var/www/html/foo.txt"
# 创建以上文件的拷贝
dst = "/tmp/foo.txt"
os.link( path, dst)
print ("创建硬链接成功!!")
"""
# ************************************************* os.listdir() ***********************************************
"""
os.listdir() 方法用于返回指定的文件夹包含的文件或文件夹的名字的列表。这个列表以字母顺序。 它不包括 '.' 和'..' 即使它在文件夹中。
只支持在 Unix, Windows 下使用。
listdir()方法语法格式如下：
    os.listdir(path)
        path -- 需要列出的目录路径
返回指定路径下的文件和文件夹列表。
"""
# ************************************************* os.mkdir() *************************************************
"""
os.mkdir() 方法用于以数字权限模式创建目录。默认的模式为 0777 (八进制)。
如果目录有多级，则创建最后一级，如果最后一级目录的上级目录有不存在的，则会抛出一个 OSError。
mkdir()方法语法格式如下：
    os.mkdir(path[, mode])
        path -- 要创建的目录，可以是相对或者绝对路径。
        mode -- 要为目录设置的权限数字模式
"""
# ************************************************* os.readlink() **********************************************
"""
os.readlink() 方法用于返回软链接所指向的文件，可能返回绝对或相对路径。
在Unix中有效
readlink()方法语法格式如下：
    os.readlink(path)
        path -- 要查找的软链接路径
返回软链接所指向的文件 

src = '/usr/bin/python'
dst = '/tmp/python'

# 创建软链接
os.symlink(src, dst)

# 使用软链接显示源链接
path = os.readlink( dst )
print (path)
"""
# ************************************************* os.remove() ************************************************
"""
os.remove() 方法用于删除指定路径的文件。如果指定的路径是一个目录，将抛出OSError。
在Unix, Windows中有效
remove()方法语法格式如下：
    os.remove(path)
        path -- 要移除的文件路径
该方法没有返回值 
"""
# ************************************************* os.removedirs() ********************************************
"""
os.removedirs() 方法用于递归删除目录。像rmdir(), 如果子文件夹为空文件夹则执行删除，成功删除, 
removedirs()才尝试它们的父文件夹<同理父文件夹也为空才执行删除>,
(直到遇到同目录下有其他文件或者文件夹停止删除)。
removedirs()方法语法格式如下：
    os.removedirs(path)
        path -- 要移除的目录路径
该方法没有返回值 
"""
# ************************************************* os.rename() ************************************************
"""
os.rename() 方法用于命名文件或目录，从 src 到 dst,如果dst是一个存在的目录, 将抛出OSError。
rename()方法语法格式如下：
    os.rename(src, dst)
        src -- 要修改的目录名
        dst -- 修改后的目录名
"""
# ************************************************* os.renames() ***********************************************
"""
os.renames() 方法用于递归重命名目录或文件。类似rename()。
renames()方法语法格式如下：
    os.renames(old, new)
        old -- 要重命名的目录
        new --文件或目录的新名字。甚至可以是包含在目录中的文件，或者完整的目录树。
说明：old 和 new路径相同，只有最后一个目录或者文件不同，则修改最后一个目录或者文件名字；要是不相同则old 路径更改为new路径
该方法没有返回值 
"""
# ************************************************* os.rmdir() *************************************************
"""
os.rmdir() 方法用于删除指定路径的目录。仅当这文件夹是空的才可以, 否则, 抛出OSError。
rmdir()方法语法格式如下：
    os.rmdir(path)
        path -- 要删除的目录路径
该方法没有返回值 
"""
# ************************************************* os.stat() **************************************************
"""
os.stat() 方法用于在给定的路径上执行一个系统 stat 的调用。
stat()方法语法格式如下：
    os.stat(path)
        path -- 指定路径
返回目标信息
print(os.stat(path))
"""
# ************************************************* os.symlink() ***********************************************
"""
os.symlink() 方法用于创建一个软链接。
symlink()方法语法格式如下：
    os.symlink(src, dst)
        src -- 源地址。
        dst -- 目标地址。
"""
# ************************************************* os.unlink() ************************************************
"""
os.unlink() 方法用于删除文件,如果文件是一个目录则返回一个错误。
unlink()方法语法格式如下：
    os.unlink(path)
        path -- 删除的文件路径
该方法没有返回值。
"""
# ************************************************* os.walk() **************************************************
"""
os.walk() 方法可以创建一个生成器，用以生成所要查找的目录及其子目录下的所有文件。
os.walk() 方法用于通过在目录树中游走输出在目录中的文件名，向上或者向下。
os.walk() 方法是一个简单易用的文件、目录遍历器，可以帮助我们高效的处理文件、目录方面的事情。
在Unix，Windows中有效。
walk()方法语法格式如下：
    os.walk(top[, topdown=True[, onerror=None[, followlinks=False]]])
        top -- 根目录下的每一个文件夹(包含它自己), 产生3-元组 (dirpath, dirnames, filenames)【文件夹路径, 文件夹名字, 文件名】。
        topdown --可选，为True或者没有指定, 一个目录的的3-元组将比它的任何子文件夹的3-元组先产生 (目录自上而下)。如果topdown为 False,
        一个目录的3-元组将比它的任何子文件夹的3-元组后产生 (目录自下而上)。
        onerror -- 可选，是一个函数; 它调用时有一个参数, 一个OSError实例。报告这错误后，继续walk,或者抛出exception终止walk。
        followlinks -- 设置为 true，则通过软链接访问目录。
该方法没有返回值。

for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        print(os.path.join(root, name))
    for name in dirs:
        print(os.path.join(root, name))
说明：目标路径下面的所有的路径，文件夹，文件都将打印出
每一层输出都是三个元素[路径], [文件夹名], [文件名] 并且都打印在对应的列表中，缺少的项则为空[]
"""
# ************************************************* os.path() **************************************************
"""
os.path.abspath(path) 	            返回绝对路径
os.path.basename(path) 	            返回文件名
os.path.commonprefix(list)      	返回list(多个路径)中，所有path共有的最长的路径
os.path.dirname(path) 	            返回文件路径
os.path.exists(path) 	            路径存在则返回True,路径损坏返回False
os.path.lexists 	                路径存在则返回True,路径损坏也返回True
os.path.expanduser(path) 	        把path中包含的"~"和"~user"转换成用户目录
os.path.expandvars(path) 	        根据环境变量的值替换path中包含的"$name"和"${name}"
os.path.getatime(path)          	返回最近访问时间（浮点型秒数）
os.path.getmtime(path) 	            返回最近文件修改时间
os.path.getctime(path)          	返回文件 path 创建时间
os.path.getsize(path) 	            返回文件大小，如果文件不存在就返回错误
os.path.isabs(path) 	            判断是否为绝对路径
os.path.isfile(path) 	            判断路径是否为文件
os.path.isdir(path) 	            判断路径是否为目录
os.path.islink(path) 	            判断路径是否为链接
os.path.ismount(path) 	            判断路径是否为挂载点
os.path.join(path1[, path2[, ...]]) 把目录和文件名合成一个路径
os.path.normcase(path)           	转换path的大小写和斜杠
os.path.normpath(path) 	            规范path字符串形式
os.path.realpath(path)          	返回path的真实路径
os.path.relpath(path[, start])  	从start开始计算相对路径
os.path.samefile(path1, path2)  	判断目录或文件是否相同
os.path.sameopenfile(fp1, fp2)    	判断fp1和fp2是否指向同一文件
os.path.samestat(stat1, stat2) 	    判断stat tuple stat1和stat2是否指向同一个文件
os.path.split(path) 	            把路径分割成 dirname 和 basename，返回一个元组
os.path.splitdrive(path)        	一般用在 windows 下，返回驱动器名和路径组成的元组
os.path.splitext(path) 	            分割路径中的文件名与拓展名
os.path.splitunc(path)          	把路径分割为加载点与文件
os.path.walk(path, visit, arg)   	遍历path，进入每个目录都调用visit函数，visit函数必须有3个参数(arg, dirname, names)，
                                    dirname表示当前目录的目录名，names代表当前目录下的所有文件名，args则为walk的第三个参数
os.path.supports_unicode_filenames 	设置是否支持unicode路径名
"""
# ************************************************* os.pardir() ************************************************
"""
os.pardir() 获取当前目录的父目录（上一级目录），以字符串形式显示目录名。
注意: Windows 和 POSIX 返回 ..。
pardir()方法语法格式如下：
os.pardir
返回当前目录的父目录，默认值为 ..。
# 输出默认值 ..
print(os.pardir)
..
# 当前工作目录
path = os.getcwd()
print("当前工作目录: ", path)
# 父目录
parent = os.path.join(path, os.pardir)  # .. 返回上级目录
# 父目录
print("\n父目录:", os.path.abspath(parent))

当前工作目录:  /Users/runoob/python
父目录: /Users/runoob
"""
