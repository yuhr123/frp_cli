#!/usr/bin/env python
import click
import configparser as cp
import os

@click.group()
def cli():
    """frp 的命令行管理工具"""
    pass

@cli.command()
@click.option('-c', '--config', 'config', default='frps.ini', required=True)
def frps(config):
    """frp 服务器配置管理"""
    if not os.path.exists(config):
        # 检查配置文件是否存在
        click.echo('配置文件不存在，请核对后再试！')
        exit()
    frps = cp.ConfigParser()
    frps.read(config)

    while True:
        click.echo('正在编辑 %s' % config)
        if click.confirm('是否继续？'):
            # 打印配置段列表
            for number, section in enumerate(frps.sections()):
                click.echo(str(number) + '> ' + section)
            number = click.prompt('请选择你要编辑的配置编号', default=0, type=int)
            section = frps.sections()[number]
            section_key_list = [key for key in frps[section]]
            while True:
                # 打印选择的配置
                click.echo('[' + section + ']')
                for number, key in enumerate(frps[section]):
                    click.echo(str(number) + '> ' + key + ' = ' + frps[section][key])
                click.echo('n> 新增记录')
                click.echo('b> 返回上级')
            
                entry_number = click.prompt('请选择你要操作的编号', default='n')
                if entry_number == 'b':
                    break
                elif entry_number == 'n':
                    # 新建项
                    option = click.prompt('请输入新配置项的名称')
                    value = click.prompt('请输入值')
                    if click.confirm('是否创建新项 %s = %s ？' % (option, value)):
                        frps[section][str(option).strip()] = str(value).strip()
                        with open(config, 'w') as f:
                            frps.write(f)
                else:
                    # 编辑选中的项
                    entry = section_key_list[int(entry_number)]
                    click.echo('正在编辑 %s' % entry)
                    click.echo('e> 编辑')
                    click.echo('d> 删除')
                    action = click.prompt('请选择操作编号')

                    if action == 'e':
                        click.echo('%s 当前值为 %s' % (entry, frps[section][entry]))
                        new_value = click.prompt('请输入新的值')
                        if click.confirm('是否将 %s 的值修改为 %s？' % (entry, new_value)):
                            frps[section][entry] = str(new_value).strip()
                            with open(config, 'w') as f:
                                frps.write(f)
                    elif action == 'd':
                        if click.confirm('是否要删除 %s ？' % entry):
                            frps.remove_option(section, entry)
                            with open(config, 'w') as f:
                                frps.write(f)
        else:
            break

if __name__ == "__main__":
    cli()
