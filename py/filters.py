"""Provides utility classes for filtering objects, such as Athletes
   or Segments
"""
from abc import abstractmethod

class AbstractFilter(object):
    """Abstract base class for filtering. Child classes can inherit from
       this class and define the filter method, which will be applied to 
       each object in the stream upon iteration.
    """
    def __init__(self, stream, **kwargs):
        self.filtered = []
        self.kwargs = kwargs if kwargs else {}
        self.stream = stream
    
    def __next__(self):
        return self.filter(self.stream.next())

    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

    @abstractmethod
    def filter(self, obj):
        pass

    def get_filtered(self):
        """Returns sequence of objects that have been filtered
        """
        return self.filtered


class ActivityFilter(AbstractFilter):
    """Filters activities based on specific kwargs
    """
    def __init__(self, stream, **kwargs):
        from stravalib import unithelper
        self.unithelper = unithelper
        AbstractFilter.__init__(self, stream, **kwargs)

    def filter(self, obj): 
        """Filter kwargs (not manual entries are also filtered):
           kwarg:      value(s)        default action
           type:       'Run','Ride'    non-run, non-ride activities filtered         
           distance:   numeric         filtered if =< 0 mile
        """
        
        activity_type = self.kwargs["type"] if self.kwargs.has_key("type") \
                        else ["Ride", "Run"]
        distance      = self.kwargs["distance"] if self.kwargs.has_key("distance") \
                        else 0
        activity_id   = True if self.kwargs.has_key("ids") else False

        if obj.manual:
            self.filtered.append( obj )
            return self.__next__()
        elif obj.type not in activity_type:
            self.filtered.append( obj )
            return self.__next__()
        elif float(self.unithelper.miles( obj.distance )) <= distance:
            self.filtered.append( obj )
            return self.__next__() 
        elif activity_id:
            return obj.id
        else:
            return obj

def filter_segment_efforts(seg_efforts, unithelper, min_miles=1, min_grade=0, 
                          ids_only=False, unique_ids=True):
    """Filters segment effort segments based on specific kwargs
    """
    filtered = []
    ids, ids_filt = set(), set()
    
    for seg_effort in seg_efforts:
        seg = seg_effort.segment
         
        if (unique_ids) and (seg.id in ids or seg.id in ids_filt): 
            continue
        if seg.average_grade < min_grade:
            ids_filt.add( seg.id )
            continue
        elif float(unithelper.miles( seg.distance )) < min_miles:
            ids_filt.add( seg.id )
            continue
        elif ids_only:
            ids.add( seg.id )
            filtered.append( seg.id )
        else:
            ids.add( seg.id )
            filtered.append( seg )
    return filtered
