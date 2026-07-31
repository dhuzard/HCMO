# Environmental, temporal, and QUDT migration

The standard HCMO profile now separates specification, observation, state
evidence, and quantity representation. No published HCMO IRI was deleted.

| Earlier representation | Current representation |
| --- | --- |
| `AmbientTemperature`, `RelativeHumidity`, gas/light shortcuts | profile `hasMeasurementSpec` specification; specification `specifiesProperty` property; observation `sosa:observedProperty` property |
| `hcm-env:hasValue` plus a unit string | `hcm-env:hasSpecifiedValue` a QUDT QuantityValue |
| `hcm-obs:hasNumericValue` plus `hcm:hasUnit` | `qudt:numericValue` plus `qudt:hasUnit` on the result node |
| numeric dimension fields plus `hasDimUnit` | one QUDT QuantityValue for each dimension role |
| `hcm-tech:hasSamplingRate` string | `hcm-tech:hasSamplingRateQuantity` a QUDT QuantityValue |
| `isOccupied` or `hasMonitoredAnimals` | query time-bounded HousingAssignment records at an explicit reference time |
| `isOperational` | OperationalStatusRecord with validity interval and generating OperationalAssessment |
| `isCalibrated` | CalibrationRecord with validity interval and generating CalibrationActivity |
| subject observation shortcut | inverse query over `sosa:hasFeatureOfInterest` |

Half-open intervals `[start, end)` are used for current-housing queries. A
value at the end instant belongs to a succeeding assignment, not both.

Example quantity:

```turtle
ex:temperature-result a hcm-obs:QuantityValue ;
  qudt:numericValue 21.8 ;
  qudt:hasUnit unit:DEG_C .
```

The JSON-LD context retains old aliases for reading legacy payloads and adds
new quantity/status aliases. Deprecation does not make legacy assertions
historical evidence: new standard-profile data must use the current patterns.

