import os
import datetime
import FileResourcesGenerator
import DataCleanerManager
import CollisionManager
import FirstIterationAggregator
import SecondIterationAggregator
import ThirdIterationAggregator



class MainApplication:

    def __init__(self):
        self.currentTime = datetime.datetime.now().replace(microsecond=0)
        print(f"Application Start At: {self.currentTime}")
        
    def Load(self):
        self.fl_rs_gen = FileResourcesGenerator.FileResourcesGenerator()
        #self.fl_rs_gen.loadAndMakePathResources()
        self.fl_rs_gen.loadJsonPathFiles()
        

        self.dt_cl_man = DataCleanerManager.DataCleanerManager(self.fl_rs_gen.getDictionary_CM_Path())
        self.dt_cl_man.cleanDataSet()
        
        self.coll_man = CollisionManager.CollisionManager()
        self.coll_man.LoadPathData(self.fl_rs_gen.getDictionary_CM_Path())
        self.coll_man.getCollisionDictionary()
        self.coll_man.getCollisionInvDictionary()
        self.coll_man.getCollisionSimDictionary()
        
        self.first_it_aggregator = FirstIterationAggregator.FirstIterationFileAggregator(self.fl_rs_gen.getDictionary_LK_Path())
        self.first_it_aggregator.RunInteration()
        #self.first_it_aggregator.LoadPath()
        self.first_it_aggregator_attr = FirstIterationAggregator.FirstIterationAttrAggregator(self.first_it_aggregator.getDictionary_LK_Path(), self.coll_man.getCollisionInvDictionary(), self.coll_man.getCollisionSimDictionary())
        self.first_it_aggregator_attr.RunInterationCleaning()

        self.second_it_aggregator = SecondIterationAggregator.SecondIterationFileAggregator(self.first_it_aggregator.getDictionary_LK_Path())
        self.second_it_aggregator.RunInteration()
        #self.second_it_aggregator.LoadPath()
        self.second_it_aggregator_attr = SecondIterationAggregator.SecondIterationAttrAggregator(self.second_it_aggregator.getDictionary_LK_Path(), self.coll_man.getCollisionInvDictionary(), self.coll_man.getCollisionSimDictionary())
        self.second_it_aggregator_attr.RunInterationCleaning()
        
        self.third_it_aggregator = ThirdIterationAggregator.ThirdIterationFileAggregator(self.second_it_aggregator.getDictionary_LK_Path())
        self.third_it_aggregator.RunInteration()
        
        

if __name__ == "__main__":
    main = MainApplication()
    main.Load()