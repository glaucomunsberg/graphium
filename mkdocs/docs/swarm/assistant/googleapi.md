# Definition

`GoogleAPI.py` get a valid key in a list of Google Console Keys.

## Params

**logger**: a instance of logger or `None`. `type:Logger`


## Methods


**get_authorization_key**: get a key from google apy list. `type:Disc`

**get_best_key_position**: Returns the best key position. `type:Int`

**authorizing_key**: Return if the `get_best_key_position` is authorized to be send a request. `type:Bool`

**time_elapsed_by_key**: return the time elapsed between start and last calculation `type:Int`

**time_do_sleep_by_key**: return seconds to sleep. `type:Int`
