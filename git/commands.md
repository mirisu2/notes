[book](https://git-scm.com/book/ru/v2)

## Install git on Debian/Ubuntu
```
apt-get install git
git --version
```
```
git config --global user.name "My name"
git config --global user.email "gde@to.tam"
git config -l
cat ~/.gitconfig

git --help
usage: git [--version] [--help] [-C <path>] [-c <name>=<value>]
           [--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
           [-p | --paginate | -P | --no-pager] [--no-replace-objects] [--bare]
           [--git-dir=<path>] [--work-tree=<path>] [--namespace=<name>]
           <command> [<args>]
These are common Git commands used in various situations:

start a working area (see also: git help tutorial)
   clone      Clone a repository into a new directory
   init       Create an empty Git repository or reinitialize an existing one

work on the current change (see also: git help everyday)
   add        Add file contents to the index
   mv         Move or rename a file, a directory, or a symlink
   reset      Reset current HEAD to the specified state
   rm         Remove files from the working tree and from the index

examine the history and state (see also: git help revisions)
   bisect     Use binary search to find the commit that introduced a bug
   grep       Print lines matching a pattern
   log        Show commit logs
   show       Show various types of objects
   status     Show the working tree status

grow, mark and tweak your common history
   branch     List, create, or delete branches
   checkout    Switch branches or restore working tree files
   commit     Record changes to the repository
   diff       Show changes between commits, commit and working tree, etc
   merge      Join two or more development histories together
   rebase     Reapply commits on top of another base tip
   tag        Create, list, delete or verify a tag object signed with GPG

collaborate (see also: git help workflows)
   fetch      Download objects and refs from another repository
   pull       Fetch from and integrate with another repository or a local branch
   push       Update remote refs along with associated objects

'git help -a' and 'git help -g' list available subcommands and some
concept guides. See 'git help <command>' or 'git help <concept>'
to read about a specific subcommand or concept.


## Инициализация git репозитория
cd myproject
git init .
git status

git add filename
or
git add .
git checkout -- <filename>... #откатить изменения
git diff --staged #показать какие изменения будут добавлены
git commit --verbose
or
git commit -m "my comment"

git log
git log -1 #show last commit
git log -1 #show last changes
git show

git clone https://github.com/mirisu2/git.git
git remote -v
git remote set-url origin git@github.com:mirisu2/git.git


git branch                       #show current branch
git branch fix_error             #create new branch
git checkout fix_error           #jump into another branch
or
git checkout -b fix_error        #create new branch & jump into new branch

git checkout master              #jump to master branch
git merge fix_error              #Join fix_error with master
git branch -d fix_error          #delete branch after joining
git branch -D fix_error          #delete branch without joining


git log #Get id
git checkout <id> #jump into N... commit

git reset --hard HEAD~2
git reset --soft HEAD~4

git push origin
git push --set-upstream origin fix_error #create remote branch on github
git push origin --delete fix_error #delete remote branch
```
