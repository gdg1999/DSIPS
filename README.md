# DSIPS
 Dynamic Sparse Identification of Power System
 
 电力系统模型实时辨识软件

版本：2023年12月

Version 2023.12

- 分支一：主分支，目前开发的分支; (Main: it will be updated;)
- 分支二：GUI分支，功能相对滞后，但具有GUI界面，可随时打包exe. (Branch1: with GUI, delayed function development, and exe package files.)

## Introduction in Brief
- This system is based on the pysindy and control package, which provides the relative optimization frame and control tools.
- It can identify the model in nonlinear or linear form, providing a convenient interface for adding the constraints.
- The structure of this system is illustrated as follows:
![052b34b37f62fd6afaa135a2be974c4](https://github.com/gdg1999/DSIPS/assets/148469282/e80288c7-ff1e-4a8d-a532-004d4183ed12)

- The system class contains the block class, also connected with the constraint class. These three classes form the basic frame for the DSIPS, stored in the Algo files.
- Other tools, like figure plots, relative analysis, control implementation, and other tools developed in the future, are stored in the Tools files.


- The data source can come from Simulink directly, which needs Matlab-engine to bridge the Simulink and Python.
- Data in Excel are also available, which should specify the variable names in the first row.

## How to use?
A toy example based on the Heffron model is provided. Three files must be prepared: Configurations.py, data source in Excel, and main.py.

- main contains the specific procedure of your work. (For me, one main for one paper)
- Configurations.py contains the block information, including the constraints, variables, and inputs. It also contains system information, including the inputs and outputs and the number of differential and algebra blocks.
- The variables in Configurations.py should match with the data source in Excel. (of course, if you use Simulink directly, the variables to the workspace should be matched with the Configurations.py)

Then, a system can be trained and analyzed. 

## Other issues...



更多功能正在研发，敬请期待！

联系人Duange Guo

详细理论与信息可关注：
https://space.bilibili.com/7829899?spm_id_from=333.1007.0.0




