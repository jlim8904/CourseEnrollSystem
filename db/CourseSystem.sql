create table Departments(
    DepartmentName varchar(255),
    CollegeName varchar(255),
    DegreeType varchar(255),
    TotalCredits int,
    CompCredits int,
    InDeptCredits int,
    OutDeptCredits int,
    GenCompCredits int,
    GenElectiveCredits int,
    primary key(DepartmentName,CollegeName,DegreeType)
);


insert into Departments(DepartmentName,CollegeName,DegreeType,TotalCredits,CompCredits,InDeptCredits,OutDeptCredits,GenCompCredits,GenElectiveCredits)values ("資訊工程學系","資電學院","學士",128,63,28,9,16,12);
insert into Departments(DepartmentName,CollegeName,DegreeType,TotalCredits,CompCredits,InDeptCredits,OutDeptCredits,GenCompCredits,GenElectiveCredits)values ("電子工程學系","資電學院","學士",130,75,27,0,16,12);
insert into Departments(DepartmentName,CollegeName,DegreeType,TotalCredits,CompCredits,InDeptCredits,OutDeptCredits,GenCompCredits,GenElectiveCredits)values ("財務金融學系","金融學院","學士",100,65,20,0,7,8);
insert into Departments(DepartmentName,CollegeName)values("通識學系","通識學院");

create table Classrooms(
    Building varchar(255),
    RoomNo  int,
    Capacity int,
    primary key(Building,RoomNo)
);


insert into Classrooms(Building,RoomNo,Capacity) values("資電",104,70);
insert into Classrooms(Building,RoomNo,Capacity) values("資電",404,20);
insert into Classrooms(Building,RoomNo,Capacity) values("科航",202,15);
insert into Classrooms(Building,RoomNo,Capacity) values("資電",403,75);
insert into Classrooms(Building,RoomNo,Capacity) values("科航",204,35);
insert into Classrooms(Building,RoomNo,Capacity) values("資電",234,80);
insert into Classrooms(Building,RoomNo,Capacity) values("資電",102,72);
insert into Classrooms(Building,RoomNo,Capacity) values("資電",402,82);
insert into Classrooms(Building,RoomNo,Capacity) values("科航",102,75);
insert into Classrooms(Building,RoomNo,Capacity) values("忠勤",103,62);
insert into Classrooms(Building,RoomNo,Capacity) values("語文",407,35);
insert into Classrooms(Building,RoomNo,Capacity) values("忠勤",207,70);
insert into Classrooms(Building,RoomNo,Capacity) values("資電",106,55);
insert into Classrooms(Building,RoomNo,Capacity) values("資電",107,65);
insert into Classrooms(Building,RoomNo,Capacity) values("資電",305,76);
insert into Classrooms(Building,RoomNo,Capacity) values("商學",311,12);
insert into Classrooms(Building,RoomNo,Capacity) values("商學",306,18);
insert into Classrooms(Building,RoomNo,Capacity) values("資電",103,75);
insert into Classrooms(Building,RoomNo,Capacity) values("忠勤",205,65);
insert into Classrooms(Building,RoomNo,Capacity) values("科航",201,72);
insert into Classrooms(Building,RoomNo,Capacity) values("商學",202,2);
insert into Classrooms(Building,RoomNo,Capacity) values("商學",203,2);



create  table Courses(
    CourseID varchar(255),
    CourseCode varchar(255),
    CourseName varchar(255),
    DepartmentName varchar(255),
    Credits int,
    CreditType varchar(255),
    years int,
    semester int,
    course_years int,
    course_classNO varchar(255),
    primary key(CourseID),
    foreign key(DepartmentName) references Departments(DepartmentName)
);


insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("1248","IECS322","資料庫系統","資訊工程學系",3,"必修",110,2,2,"乙");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("1247","IECS203","系統程式","資訊工程學系",3,"必修",110,2,2,"乙");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("1241","IECS203","系統程式","資訊工程學系",3,"必修",110,2,2,"甲");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("1249","IECS225","機率與統計","資訊工程學系",3,"必修",110,2,2,"乙");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("1246","UNIV902","班級活動","資訊工程學系",0,"必修",110,2,2,"乙");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("1245","IECS206","unix應用與實務","資訊工程學系",2,"選修",110,2,2,"乙");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("1260","IECS241","互連網路","資訊工程學系",3,"選修",110,2,2,"乙");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("1262","IECS226","電子商務安全","資訊工程學系",3,"選修",110,2,2,"合");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("1263","IECS233","數位信號處理導論","資訊工程學系",3,"選修",110,2,2,"乙");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("1264","IECS253","數位系統設計","資訊工程學系",3,"選修",110,2,2,"乙");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("1265","IECS214","數位系統設計實驗","資訊工程學系",1,"選修",110,2,2,"乙");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("3449","MILT135","國防科技","資訊工程學系",1,"必修",110,2,2,"乙");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("1254","IECS211","系統分析與設計","資訊工程學系",3,"選修",110,2,2,"乙");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("1244","IECS211","系統分析與設計","資訊工程學系",3,"選修",110,2,2,"乙");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("1261","IECS353","組合數學","資訊工程學系",3,"選修",110,2,2,"合");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("1409","ELEN203","電子學","電子工程學系",13,"必修",110,2,2,"甲");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("1412","ELEN210","電磁學","電子工程學系",13,"必修",110,2,2,"甲");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("1425","ELEN216","積體電路","電子工程學系",8,"必修",110,2,2,"乙");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("1416","ELEN201","工程數學","電子工程學系",3,"必修",110,2,2,"乙");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("1896","ELEN308","半導體","電子工程學系",8,"必修",110,2,3,"半導體學程");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("0249","ACCT112","會計學","財務金融學系",3,"必修",110,2,1,"乙");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("0258","ECON110","經纃學","財務金融學系",3,"必修",110,2,1,"丙");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("0264","INSU101","保險學","財務金融學系",3,"必修",110,2,2,"甲");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("3188","LCO46","大二英文","資訊工程學系",1,"必修",110,2,2,"英文綜合班");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("0299","FINA320","期貨與選擇權","財務金融學系",3,"選修",110,2,3,"丙");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("2811","GHUEE12","台灣民俗文化","通識學系",2,"選修",110,2,2,"通識");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("2812","GHUEE13","莎士比亞與電影","通識學系",2,"選修",110,2,2,"通識");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("3312","GHIN166","中文思辦與表達","通識學系",2,"選修",110,2,2,"國文綜合班");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("3187","LCO46","大二英文","資訊工程學系",1,"必修",110,2,2,"英文綜合班");
insert into Courses(CourseID,CourseCode,CourseName,DepartmentName,Credits,CreditType,years,semester,course_years,course_classNO) values("2925","GMII339","原住民音樂文化專題","通識學系",2,"選修",110,2,2,"通識");







create table Prereqs(
    CourseID varchar(255),
    PrereqsID varchar(255),
    primary key(CourseID,PrereqsID),
    foreign key(CourseID) references Courses(CourseID),
    foreign key(PrereqsID) references Courses(CourseID)
);


create table TimeSlot(
    TimeSlotID varchar(255),
    T_Day varchar(255),
    StartTime int,
    Endtime int,
    primary key(TimeSlotID)
);


insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("a1","一",8,9);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("a2","一",9,10);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("a3","一",10,11);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("a4","一",11,12);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("a5","一",12,13);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("a6","一",13,14);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("a7","一",14,15);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("a8","一",15,16);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("a9","一",16,17);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("a10","一",17,18);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("b1","二",8,9);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("b2","二",9,10);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("b3","二",10,11);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("b4","二",11,12);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("b5","二",12,13);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("b6","二",13,14);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("b7","二",14,15);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("b8","二",15,16);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("b9","二",16,17);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("b10","二",17,18);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("c1","三",8,9);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("c2","三",9,10);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("c3","三",10,11);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("c4","三",11,12);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("c5","三",12,13);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("c6","三",13,14);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("c7","三",14,15);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("c8","三",15,16);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("c9","三",16,17);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("c10","三",17,18);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("c11","三",18,19);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("c12","三",19,20);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("c13","三",20,21);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("d1","四",8,9);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("d2","四",9,10);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("d3","四",10,11);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("d4","四",11,12);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("d5","四",12,13);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("d6","四",13,14);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("d7","四",14,15);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("d8","四",15,16);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("d9","四",16,17);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("d10","四",17,18);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("e1","五",8,9);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("e2","五",9,10);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("e3","五",10,11);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("e4","五",11,12);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("e5","五",12,13);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("e6","五",13,14);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("e7","五",14,15);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("e8","五",15,16);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("e9","五",16,17);
insert into TimeSlot(TimeSlotID,T_Day,StartTime,Endtime)values("e10","五",17,18);


create table Sections(
    CourseID varchar(255),
    TimeSlotID varchar(255),
    Semester int,
    Years int,
    Building varchar(255),
    RoomNo int,
    primary key(CourseID,TimeSlotID,Semester,Years),
    foreign key(CourseID) references Courses(CourseID),
    foreign key(TimeSlotID) references TimeSlot(TimeSlotID),
    foreign key(Building,RoomNo) references Classrooms(Building,RoomNo)
);


insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1248","a4",2,110,"資電",104);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1248","d6",2,110,"資電",404);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1248","d7",2,110,"資電",404);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1241","a3",2,110,"資電",404);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1241","a4",2,110,"資電",404);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1241","b3",2,110,"資電",404);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1247","a2",2,110,"忠勤",205);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1247","a3",2,110,"忠勤",205);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1247","d8",2,110,"科航",202);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1249","b3",2,110,"資電",403);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1249","d3",2,110,"科航",204);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1249","d4",2,110,"科航",204);
insert into Sections(CourseID,TimeSlotID,Semester,Years)values("1246","a10",2,110);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1245","d9",2,110,"資電",234);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1245","d10",2,110,"資電",234);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1260","a6",2,110,"資電",234);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1260","a7",2,110,"資電",234);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1260","a8",2,110,"資電",234);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1262","c11",2,110,"科航",202);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1262","c12",2,110,"科航",202);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1262","c13",2,110,"科航",202);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1263","a8",2,110,"資電",102);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1263","a9",2,110,"資電",102);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1263","c3",2,110,"資電",103);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1264","a1",2,110,"資電",104);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1264","b7",2,110,"資電",402);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1264","b8",2,110,"資電",402);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1265","b9",2,110,"資電",234);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1265","b10",2,110,"資電",234);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("3449","c1",2,110,"科航",102);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("3449","c2",2,110,"科航",102);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1254","b9",2,110,"資電",403);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1254","c8",2,110,"資電",104);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1254","c9",2,110,"資電",104);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1244","b8",2,110,"資電",403);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1244","c6",2,110,"資電",104);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1244","c7",2,110,"資電",104);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1261","c6",2,110,"忠勤",103);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1261","c7",2,110,"忠勤",103);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1261","d2",2,110,"忠勤",103);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1409","c3",2,110,"語文",407);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1409","c4",2,110,"語文",407);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1409","d6",2,110,"語文",407);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1412","c6",2,110,"忠勤",207);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1412","c7",2,110,"忠勤",207);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1412","d7",2,110,"語文",407);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1425","a8",2,110,"資電",106);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1425","a9",2,110,"資電",106);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1425","c2",2,110,"資電",107);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1416","b1",2,110,"資電",103);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1416","b2",2,110,"資電",103);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1416","d2",2,110,"資電",104);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1896","a3",2,110,"資電",305);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1896","a4",2,110,"資電",305);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("1896","b6",2,110,"商學",202);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("0249","a6",2,110,"商學",311);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("0249","a7",2,110,"商學",311);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("0249","a8",2,110,"商學",311);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("0258","e2",2,110,"商學",203);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("0258","e3",2,110,"商學",203);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("0258","e4",2,110,"商學",203);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("0264","c6",2,110,"商學",306);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("0264","c7",2,110,"商學",306);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("0264","c8",2,110,"商學",306);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("3188","e2",2,110,"商學",306);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("3188","e3",2,110,"商學",306);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("3188","e4",2,110,"商學",306);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("3187","e2",2,110,"商學",311);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("3187","e3",2,110,"商學",311);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("3187","e4",2,110,"商學",311);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("2925","b6",2,110,"資電",104);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("2925","b7",2,110,"資電",104);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("0299","c2",2,110,"商學",306);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("0299","c3",2,110,"商學",306);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("0299","c4",2,110,"商學",306);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("3312","e1",2,110 ,"語文",407);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("3312","e2",2,110 ,"語文",407);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("2812","e6",2,110 ,"忠勤",207);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("2812","e7",2,110 ,"忠勤",207);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("2811","a6",2,110 ,"語文",407);
insert into Sections(CourseID,TimeSlotID,Semester,Years,Building,RoomNo)values("2811","a7",2,110 ,"語文",407);






create table ClassroomCourses(
    Building varchar(255),
    RoomNo  int,
    CourseID varchar(255),
    TimeSlotID varchar(255),
    Semester int,
    Years int,
    primary key(Building,RoomNo,CourseID,TimeSlotID,Semester,Years),
    foreign key(Building,RoomNo) references Classrooms(Building,RoomNo),
    foreign key(CourseID,TimeSlotID,Semester,Years) references Sections(CourseID,TimeSlotID,Semester,Years)
);


create table Lecturers(
    LecturerID varchar(255),
    LecturerName varchar(255),
    DepartmentName varchar(255),
    primary key(LecturerID),
    foreign key(DepartmentName) references Departments(DepartmentName)
);


insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T1","劉明機","資訊工程學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T2","林峰正","資訊工程學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T3","陳小琪","電子工程學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T4","王一二","財務金融學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T5","劉宗杰","資訊工程學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T6","許懷中","資訊工程學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T7","劉怡芬","資訊工程學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T8","游景盛","資訊工程學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T9","周澤捷","資訊工程學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T10","陳啟鏘","資訊工程學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T11","陳德生","資訊工程學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T12","王金輝","資訊工程學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T13","洪振偉","資訊工程學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T14","許恒壽","電子工程學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T15","施仁斌","電子工程學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T16","楊炳章","電子工程學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T17","康宗貴","電子工程學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T18","李景松","電子工程學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T19","吳東憲","財務金融學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T20","林晉禾","財務金融學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T21","吳仰哲","財務金融學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T22","謝孟成","通識學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T23","林慧咨","通識學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T24","林芷瑩","資訊工程學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T25","戴文嫻","通識學系");
insert into Lecturers(LecturerID,LecturerName,DepartmentName)values("T26","daneil","資訊工程學系");



create table Classes(
    DepartmentName varchar(255),
    ClassNo varchar(255),
    Years int,
    semester int,
    class_year int,
    ClassTutor varchar(255),
    primary key(ClassNo,DepartmentName,Years),
    foreign key(DepartmentName) references Departments(DepartmentName),
    foreign key(ClassTutor) references Lecturers(LecturerID)
);


insert into Classes(DepartmentName,ClassNo,Years,class_year,semester,ClassTutor) values("資訊工程學系","乙",110,2,2,"T1");
insert into Classes(DepartmentName,ClassNo,Years,class_year,semester,ClassTutor) values("資訊工程學系","乙",109,1,2,"T2");
insert into Classes(DepartmentName,ClassNo,Years,class_year,semester,ClassTutor) values("資訊工程學系","甲",110,2,2,"T3");
insert into Classes(DepartmentName,ClassNo,Years,class_year,semester,ClassTutor) values("資訊工程學系","丙",110,2,2,"T4");
insert into Classes(DepartmentName,ClassNo,Years,class_year,semester,ClassTutor) values("資訊工程學系","丁",110,2,2,"T5");
insert into Classes(DepartmentName,ClassNo,Years,class_year,semester,ClassTutor) values("資訊工程學系","戊",110,2,2,"T6");
insert into Classes(DepartmentName,ClassNo,Years,class_year,semester,ClassTutor) values("資訊工程學系","已",110,2,2,"T7");
insert into Classes(DepartmentName,ClassNo,Years,class_year,semester,ClassTutor) values("資訊工程學系","庚",110,2,2,"T8");
insert into Classes(DepartmentName,ClassNo,Years,class_year,semester,ClassTutor) values("資訊工程學系","辛",110,2,2,"T9");
insert into Classes(DepartmentName,ClassNo,Years,class_year,semester,ClassTutor) values("資訊工程學系","壬",110,2,2,"T10");
insert into Classes(DepartmentName,ClassNo,Years,class_year,semester,ClassTutor) values("資訊工程學系","癸",110,2,2,"T11");
insert into Classes(DepartmentName,ClassNo,Years,class_year,semester,ClassTutor) values("資訊工程學系","A",110,2,2,"T12");
insert into Classes(DepartmentName,ClassNo,Years,class_year,semester,ClassTutor) values("資訊工程學系","B",110,2,2,"T13");
insert into Classes(DepartmentName,ClassNo,Years,class_year,semester,ClassTutor) values("電子工程學系","甲",110,2,2,"T14");
insert into Classes(DepartmentName,ClassNo,Years,class_year,semester,ClassTutor) values("電子工程學系","乙",110,2,2,"T15");
insert into Classes(DepartmentName,ClassNo,Years,class_year,semester,ClassTutor) values("電子工程學系","丙",110,2,2,"T16");
insert into Classes(DepartmentName,ClassNo,Years,class_year,semester,ClassTutor) values("電子工程學系","丁",110,2,2,"T17");
insert into Classes(DepartmentName,ClassNo,Years,class_year,semester,ClassTutor) values("電子工程學系","戊",110,2,2,"T18");
insert into Classes(DepartmentName,ClassNo,Years,class_year,semester,ClassTutor) values("財務金融學系","甲",110,2,2,"T19");
insert into Classes(DepartmentName,ClassNo,Years,class_year,semester,ClassTutor) values("財務金融學系","乙",110,2,2,"T20");
insert into Classes(DepartmentName,ClassNo,Years,class_year,semester,ClassTutor) values("財務金融學系","丙",110,2,2,"T21");



create table Students(
    StudentID varchar(255),
    StudentName varchar(255),
    DepartmentName varchar(255),
    ClassNo varchar(255),
    Years int,
    semester int,
    students_year int,
    TotalCredits int,
    CompCredits int,
    InDeptCredits int,
    OutDeptCredits int,
    GenCompCredits int,
    GenElectiveCredits int,
    primary key(StudentID),
    foreign key(DepartmentName) references Departments(DepartmentName),
    foreign key(ClassNo) references Classes(ClassNo)
);


insert into Students(StudentID,StudentName,DepartmentName,ClassNo,Years,semester,students_year) values("D0909709","林子權","資訊工程學系","乙",110,2,2);
insert into Students(StudentID,StudentName,DepartmentName,ClassNo,Years,semester,students_year) values("D0948333","彭彥程","資訊工程學系","乙",110,2,2);
insert into Students(StudentID,StudentName,DepartmentName,ClassNo,Years,semester,students_year) values("D1077776","張芳榳","資訊工程學系","乙",110,2,2);
insert into Students(StudentID,StudentName,DepartmentName,ClassNo,Years,semester,students_year) values("D1077780","王小明","電子工程學系","甲",110,2,2);
insert into Students(StudentID,StudentName,DepartmentName,ClassNo,Years,semester,students_year) values("D1000001","戴子琪","資訊工程學系","甲",110,2,2);
insert into Students(StudentID,StudentName,DepartmentName,ClassNo,Years,semester,students_year) values("D1000002","陳紫伶","財務金融學系","丙",110,2,1);



create table Takes(
    StudentID varchar(255),
    CourseID varchar(255),
    TimeSlotID varchar(255),
    Semester int,
    Years int,
    CreditType varchar(255),
    score float,
    primary key(StudentID,CourseID,TimeSlotID,Semester,Years),
    foreign key(StudentID) references Students(StudentID),
    foreign key(CourseID,TimeSlotID,Semester,Years)references Sections(CourseID,TimeSlotID,Semester,Years)
);


-- insert into Takes(StudentID,CourseID,TimeSlotID,Semester,Years,CreditType,score) values("D0909709","IECS0000","a4",2,2,"必修",98);
-- insert into Takes(StudentID,CourseID,TimeSlotID,Semester,Years,CreditType,score) values("D0909709","BB0001","a2",1,2,"選修",90);
-- insert into Takes(StudentID,CourseID,TimeSlotID,Semester,Years,CreditType,score) values("D0948333","IECS0002","a2",2,2,"必修",90);
-- insert into Takes(StudentID,CourseID,TimeSlotID,Semester,Years,CreditType,score) values("D1077780","EE0000","a2",2,2,"必修",96);
-- insert into Takes(StudentID,CourseID,TimeSlotID,Semester,Years,CreditType) values("D1077780","BB0002","c4",2,2,"選修");
-- insert into Takes(StudentID,CourseID,TimeSlotID,Semester,Years,CreditType,score) values("D1077780","EE0001","d6",2,2,"必修",75);
-- insert into Takes(StudentID,CourseID,TimeSlotID,Semester,Years,CreditType,score) values("D1077780","EE0002","d7",2,2,"必修",70);
-- insert into Takes(StudentID,CourseID,TimeSlotID,Semester,Years,CreditType,score) values("D1077780","EE0003","d8",2,2,"必修",63);
-- insert into Takes(StudentID,CourseID,TimeSlotID,Semester,Years,CreditType,score) values("D1077780","EE0004","e2",2,2,"必修",89);
-- insert into Takes(StudentID,CourseID,TimeSlotID,Semester,Years,CreditType,score) values("D1077776","IECS0005","b3",2,2,"必修",85);
-- insert into Takes(StudentID,CourseID,TimeSlotID,Semester,Years,CreditType) values("D1000001","BB0000","c6",2,2,"選修");
-- insert into Takes(StudentID,CourseID,TimeSlotID,Semester,Years,CreditType) values("D1000002","BB0000","c6",2,2,"必修");


create table Teaches(
    LecturerID varchar(255),
    LecturerName varchar(255),
    DepartmentName varchar(255),
    primary key(LecturerID),
    foreign key(LecturerID) references Lecturers(LecturerID),
    foreign key(DepartmentName)references Departments(DepartmentName)
);


create table UserID(
    StudentID varchar(255),
    IDPassword varchar(255),
    primary key(StudentID,IDPassword),
    foreign key(StudentID) references Students(StudentID)   
);


insert into UserID values('D0909709','709');
insert into UserID values('D0948333','333');
insert into UserID values('D1077776','776');
insert into UserID values('D1077780','780');
insert into UserID values('D1000001','001');
insert into UserID values('D1000002','002');


create table Follows(
    StudentID varchar(255),
    CourseID varchar(255),
    primary key(StudentID,CourseID),
    foreign key(StudentID) references Students(StudentID),
    foreign key(CourseID) references Courses(CourseID)  
);


create table CourseQueue(
    StudentID varchar(255),
    CourseID varchar(255),
    TimeQueue varchar(255),
    primary key(StudentID,CourseID),
    foreign key(StudentID) references Students(StudentID),
    foreign key(CourseID) references Courses(CourseID)  
);
