package com.example.studyflowapp.planner

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import com.example.studyflowapp.auth.AuthRepository
import com.example.studyflowapp.auth.AuthFailure
import org.json.JSONObject
import java.util.concurrent.Executors

data class PlannerState(val data: JSONObject? = null, val busy: Boolean = false,
    val error: String? = null, val expired: Boolean = false, val operation: String? = null)

class PlannerViewModel(app: Application) : AndroidViewModel(app) {
    private val executor = Executors.newSingleThreadExecutor()
    private val mutable = MutableLiveData(PlannerState())
    val state: LiveData<PlannerState> = mutable
    fun load(force: Boolean = false) {
        if (mutable.value?.busy == true || (!force && mutable.value?.data != null)) return
        execute(null, null)
    }
    fun save(kind: String, data: JSONObject, id: Long?, operation: String) {
        val body = JSONObject().put("kind", kind).put("action", "save").put("data", data)
        id?.let { body.put("id", it) }; execute(body, operation)
    }
    fun delete(kind: String, id: Long?, operation: String) {
        val body = JSONObject().put("kind", kind).put("action", "delete")
        id?.let { body.put("id", it) }; execute(body, operation)
    }
    fun saveLessons(items: List<JSONObject>, operation: String) {
        require(items.isNotEmpty())

        val previous = mutable.value ?: PlannerState()
        if (previous.busy) return

        mutable.value = previous.copy(
            busy = true,
            error = null,
            operation = operation
        )

        executor.execute {
            var latest = previous.data
            var saved = 0
            var failure: Exception? = null

            try {
                val repository = AuthRepository.get(getApplication())

                for (lesson in items) {
                    val body = JSONObject()
                        .put("kind", "lessons")
                        .put("action", "save")
                        .put("data", lesson)

                    latest = repository.planner(body)
                    saved++
                }
            } catch (error: Exception) {
                failure = error
            }

            val next = if (failure == null) {
                PlannerState(
                    data = latest,
                    operation = operation
                )
            } else {
                val reason = failure?.message ?: "Unknown server error"
                val message = if (saved > 0) {
                    "Saved $saved of ${items.size} lessons. Remaining lessons were not saved: $reason"
                } else {
                    reason
                }

                PlannerState(
                    data = latest ?: previous.data,
                    error = message,
                    expired = (failure as? AuthFailure)?.expired == true,
                    operation = operation
                )
            }

            mutable.postValue(next)
        }
    }

    private fun execute(body: JSONObject?, operation: String?) {
        val previous = mutable.value ?: PlannerState()
        if (previous.busy) return
        mutable.value = previous.copy(busy = true, error = null, operation = operation)
        executor.execute {
            val next = try {
                PlannerState(data = AuthRepository.get(getApplication()).planner(body), operation = operation)
            } catch (e: Exception) {
                previous.copy(busy = false, operation = operation, error = e.message ?: "Could not load your planner.",
                    expired = (e as? AuthFailure)?.expired == true)
            }
            mutable.postValue(next)
        }
    }
    override fun onCleared() { executor.shutdownNow() }
}
